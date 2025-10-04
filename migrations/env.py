import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from app.core.settings import settings
from app.models.note_model import Base

# alembic config object
config = context.config

# setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# setup database URL from pydantic settings
config.set_main_option("sqlalchemy.url", settings.database_url)

# autogeneration
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Generate SQL migration scripts without connecting to the database.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """
    Execute migrations directly against the database using an active connection.
    """
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:

        def run_migrations(sync_conn: Connection) -> None:
            context.configure(connection=sync_conn, target_metadata=target_metadata)
            with context.begin_transaction():
                context.run_migrations()

        await connection.run_sync(run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
