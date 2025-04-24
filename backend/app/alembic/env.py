import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from dotenv import load_dotenv
load_dotenv()

# Alembic Config object
config = context.config

# Set up loggers
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# === Load and fix DB URL for Alembic ===
# Use ASYNC db in app, but SYNC one for Alembic (must be psycopg2)
raw_url = os.getenv("DATABASE_URL")

# Convert asyncpg -> psycopg2 for Alembic to work
if raw_url and raw_url.startswith("postgresql+asyncpg"):
    sync_url = raw_url.replace("postgresql+asyncpg", "postgresql+psycopg2")
else:
    sync_url = raw_url

if sync_url:
    config.set_main_option("sqlalchemy.url", sync_url)

# === Import your Base metadata ===
from app.models import Base  # adjust if it's under app.models or similar
target_metadata = Base.metadata

# === Run migrations ===
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
