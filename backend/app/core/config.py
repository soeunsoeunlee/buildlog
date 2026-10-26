from functools import lru_cache
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DATABASE_PATH = PROJECT_ROOT / "database" / "buildlog.sqlite3"
DEFAULT_DATABASE_URL = f"sqlite:///{DEFAULT_DATABASE_PATH.as_posix()}"


class Settings(BaseSettings):
    app_name: str = "BuildLog API"
    app_env: str = "development"
    api_prefix: str = "/api"
    frontend_origin: str = "http://localhost:5173"

    database_url: str = DEFAULT_DATABASE_URL
    test_database_url: str = "sqlite+pysqlite:///:memory:"
    auth_secret_key: str | None = None

    @field_validator("database_url", mode="before")
    @classmethod
    def resolve_project_relative_sqlite_url(cls, value: object) -> object:
        prefix = "sqlite:///./"
        if isinstance(value, str) and value.startswith(prefix):
            relative_path = value.removeprefix(prefix)
            return f"sqlite:///{(PROJECT_ROOT / relative_path).as_posix()}"
        return value

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
