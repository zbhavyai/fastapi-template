from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from app.core.settings import settings

engine = create_async_engine(
    settings.database_url,
    pool_pre_ping=settings.database_pool_pre_ping,
    future=True,
    echo=settings.database_echo,
)

async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession]:
    async with async_session_factory() as db_session:
        yield db_session
