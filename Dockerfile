# ─────────────────────────────────────────
# Dockerfile — FastAPI + Alembic auto-migrate
# repo root → build context “.” (default on Railway)
# ─────────────────────────────────────────
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# ── Paths ─────────────────────────────────
ENV VENV_PATH="/app/.venv"
ENV PATH="$VENV_PATH/bin:$PATH"
ENV PYTHONPATH="/app"

# ── OS deps ───────────────────────────────
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential gcc libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# ── virtual-env ───────────────────────────
RUN python -m venv "${VENV_PATH}"

# ── Python deps ───────────────────────────
COPY ./backend/requirements.txt /app/requirements.txt
RUN "${VENV_PATH}/bin/pip" install --upgrade pip && \
    "${VENV_PATH}/bin/pip" install -r /app/requirements.txt

# ── Application code ──────────────────────
COPY ./backend/app       /app/app
COPY ./backend/scripts   /app/scripts

# ── Alembic config & migrations (correct paths) ──────────
COPY ./backend/alembic.ini      /app/alembic.ini
COPY ./backend/app/alembic      /app/alembic

# make entry-point executable
RUN chmod +x /app/scripts/entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/app/scripts/entrypoint.sh"]
