#!/usr/bin/env bash
set -e

# Activate the virtual-env so alembic/uvicorn use the right interpreter
source /app/.venv/bin/activate

echo "⏩ Generating new Alembic revision (autogenerate)..."
alembic revision --autogenerate -m "auto migration from entrypoint" || true   # no-op if nothing changed

echo "⏫ Running Alembic migrations..."
alembic upgrade head

echo "🚀 Starting Uvicorn ..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
