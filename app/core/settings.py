from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # -------------------------------------------------------------------------
    # LOGGING
    # -------------------------------------------------------------------------
    log_level: str = "INFO"
    log_file: Path = Path.home() / ".fastapitemplate" / "app.log"
    log_file_max_size: int = 25 * 1024 * 1024
    log_file_backup_count: int = 7
    log_format: str = "%(asctime)s [%(levelname)7s] (%(lineno)4d) %(funcName)s: %(message)s"

    # -------------------------------------------------------------------------
    # HTTP and CORS
    # -------------------------------------------------------------------------
    app_host: str = "0.0.0.0"
    app_port: int = 8080
    root_path: str = "/api"
    cors_origins: list[str] = ["*"]

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


settings = Settings()
