import asyncio
import uuid
from collections.abc import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer

from app.core.db import get_db
from app.core.settings import settings
from app.main import app
from app.models.note_model import Note


@pytest.fixture(scope="session")
def postgres_container() -> Generator[PostgresContainer]:
    container = PostgresContainer(
        "docker.io/library/postgres:17.0",
        username="appuser",
        password="apppass",
        dbname="appdb",
    )
    container.start()
    yield container
    container.stop()


@pytest_asyncio.fixture(scope="session")
async def db_engine(postgres_container: PostgresContainer) -> AsyncGenerator[AsyncEngine]:
    url = (
        f"postgresql+asyncpg://{postgres_container.username}:"
        f"{postgres_container.password}@"
        f"{postgres_container.get_container_host_ip()}:"
        f"{postgres_container.get_exposed_port(postgres_container.port)}/"
        f"{postgres_container.dbname}"
    )
    settings.database_url = url
    print("Test database URL:", url)
    engine: AsyncEngine = create_async_engine(url, future=True, echo=False)

    def run_migrations() -> None:
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", url)
        command.upgrade(alembic_cfg, "head")

    await asyncio.to_thread(run_migrations)

    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def async_session_maker(db_engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(db_engine, expire_on_commit=False, class_=AsyncSession)


@pytest_asyncio.fixture(autouse=True)
async def override_get_db(
    async_session_maker: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[None]:
    async def _get_db() -> AsyncGenerator[AsyncSession]:
        async with async_session_maker() as session:
            yield session

    app.dependency_overrides[get_db] = _get_db
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(autouse=True)
async def seed_data(
    async_session_maker: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[None]:
    async with async_session_maker() as session:
        await session.execute(text("TRUNCATE TABLE notes RESTART IDENTITY CASCADE"))

        notes = [
            Note(
                id=uuid.UUID("3282249b-19ee-4c5e-9be2-b9f714610aa6"),
                title="Note 1",
                content="Content 1",
            ),
            Note(
                id=uuid.UUID("1d7539f9-e9b7-4a06-9e6c-d5d6cf74d87a"),
                title="Note 2",
                content="Content 2",
            ),
            Note(
                id=uuid.UUID("e969ffd7-b4ce-47e1-8f43-8811ae576392"),
                title="Note 3",
                content="Content 3",
            ),
        ]
        session.add_all(notes)
        await session.commit()
    yield


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
