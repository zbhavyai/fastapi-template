import logging
import os
import tomllib
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from logging.handlers import RotatingFileHandler
from pathlib import Path

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.settings import settings


def configure_logging() -> None:
    level = getattr(logging, settings.log_level.upper())
    handlers: list[logging.Handler] = [logging.StreamHandler()]

    if settings.log_file:
        log_file = os.path.expandvars(str(settings.log_file))
        log_file = str(Path(log_file).expanduser())

        Path(log_file).parent.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=settings.log_file_max_size,
            backupCount=settings.log_file_backup_count,
        )
        handlers.append(file_handler)

    logging.basicConfig(
        level=level,
        format=settings.log_format,
        handlers=handlers,
    )


def get_project_metadata() -> dict[str, str]:
    pyproject_path = Path(__file__).resolve().parents[1] / "pyproject.toml"
    with pyproject_path.open("rb") as f:
        pyproject = tomllib.load(f)
    project = pyproject.get("project", {})
    return {
        "title": project.get("name", ""),
        "description": project.get("description", ""),
        "version": project.get("version", "1.0.0"),
    }


metadata = get_project_metadata()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    configure_logging()
    logging.info("--------------------------------------------------------------------------------")
    logging.info("Starting application")
    logging.info("--------------------------------------------------------------------------------")

    yield

    logging.info("--------------------------------------------------------------------------------")
    logging.info("Shutting down application")
    logging.info("--------------------------------------------------------------------------------")


app = FastAPI(
    title=metadata["title"],
    description=metadata["description"],
    version=metadata["version"],
    root_path=settings.root_path,
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=api_router)
