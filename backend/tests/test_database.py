from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import Session

from app.core.config import PROJECT_ROOT, Settings
from app.db.session import create_db_engine


BACKEND_ROOT = Path(__file__).resolve().parents[1]


def sqlite_url(path: Path) -> str:
    return f"sqlite:///{path.as_posix()}"


def test_project_relative_sqlite_url_is_independent_of_working_directory() -> None:
    settings = Settings(
        database_url="sqlite:///./database/buildlog.sqlite3",
        _env_file=None,
    )

    assert settings.database_url == sqlite_url(PROJECT_ROOT / "database" / "buildlog.sqlite3")


def test_sqlite_engine_connects_and_enables_foreign_keys(tmp_path: Path) -> None:
    database_path = tmp_path / "engine-test.sqlite3"
    engine = create_db_engine(sqlite_url(database_path))

    with Session(engine) as session:
        assert session.execute(text("SELECT 1")).scalar_one() == 1
        assert session.execute(text("PRAGMA foreign_keys")).scalar_one() == 1

    engine.dispose()
    assert database_path.exists()


def test_alembic_initial_migration_upgrades_and_downgrades(tmp_path: Path) -> None:
    database_path = tmp_path / "migration-test.sqlite3"
    database_url = sqlite_url(database_path)
    config = Config(str(BACKEND_ROOT / "alembic.ini"))
    config.set_main_option("script_location", str(BACKEND_ROOT / "alembic"))
    config.set_main_option("sqlalchemy.url", database_url)

    command.upgrade(config, "head")

    engine = create_engine(database_url)
    assert set(inspect(engine).get_table_names()) >= {
        "alembic_version",
        "users",
        "auth_sessions",
        "study_records",
        "todo_records",
        "error_records",
    }
    with engine.connect() as connection:
        assert connection.execute(text("SELECT version_num FROM alembic_version")).scalar_one() == "0003_records"
    engine.dispose()

    command.downgrade(config, "base")

    engine = create_engine(database_url)
    with engine.connect() as connection:
        assert connection.execute(text("SELECT COUNT(*) FROM alembic_version")).scalar_one() == 0
    engine.dispose()
