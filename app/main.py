import logging
import tomllib
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from logging.handlers import RotatingFileHandler
from pathlib import Path

from fastapi import FastAPI


def configure_logging(log_level: str, log_file: str) -> None:
    level = getattr(logging, log_level, logging.INFO)
    handlers: list[logging.Handler] = [logging.StreamHandler()]

    if log_file:
        file_handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=7)
        handlers.append(file_handler)

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)7s] (%(lineno)4d) %(funcName)s: %(message)s",
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
    configure_logging(log_level="INFO", log_file=".fastapitemplate/app.log")
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
    root_path="/api",
    lifespan=lifespan,
)
