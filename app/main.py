import logging
import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from importlib.metadata import PackageMetadata, PackageNotFoundError, metadata, version
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
    try:
        meta: PackageMetadata = metadata("fastapi-template")
        return {
            "title": meta["Name"],
            "description": meta.get("Summary", ""),
            "version": version("fastapi-template"),
        }
    except PackageNotFoundError:
        return {
            "title": "fastapi-template",
            "description": "",
            "version": "0.0.0",
        }


project_metadata = get_project_metadata()
configure_logging()


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncIterator[None]:
    logger = logging.getLogger("app.main")
    logger.info("--------------------------------------------------------------------------------")
    logger.info("Starting application")
    logger.info("--------------------------------------------------------------------------------")

    yield

    logger.info("--------------------------------------------------------------------------------")
    logger.info("Shutting down application")
    logger.info("--------------------------------------------------------------------------------")


app = FastAPI(
    title=project_metadata["title"],
    description=project_metadata["description"],
    version=project_metadata["version"],
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=api_router, prefix="/api")
