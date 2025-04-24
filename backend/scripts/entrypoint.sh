#!/usr/bin/env bash
set -e
source /app/.venv/bin/activate

# Point Alembic at the right ini file
ALEMBIC_CFG="/app/alembic.ini"

echo "⏩ Generating new Alembic revision (autogenerate)…"
alembic -c "$ALEMBIC_CFG" revision --autogenerate -m "auto migration" || true

echo "⏫ Applying migrations…"
alembic -c "$ALEMBIC_CFG" upgrade head

echo "🚀 Launching Uvicorn…"
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
