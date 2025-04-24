# ─────────────────────────────────────────────────────────────
# Dockerfile — FastAPI backend with Alembic auto-migrations
# context: repo root (build with `docker build .`)
# ─────────────────────────────────────────────────────────────
FROM python:3.10-slim

# --- Basic runtime flags ----------------------------------------------------
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# --- Paths & virtual-env ----------------------------------------------------
ENV VENV_PATH="/app/.venv"
ENV PATH="$VENV_PATH/bin:$PATH"
ENV PYTHONPATH="/app"

RUN python -m venv "${VENV_PATH}"

# --- System dependencies ----------------------------------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential gcc libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# --- Python requirements ----------------------------------------------------
COPY ./backend/requirements.txt /app/requirements.txt
RUN "${VENV_PATH}/bin/pip" install --upgrade pip && \
    "${VENV_PATH}/bin/pip" install -r /app/requirements.txt

# --- Source code & config ---------------------------------------------------
COPY ./backend/app            /app/app
COPY ./backend/scripts        /app/scripts
COPY ./backend/alembic.ini    /app/alembic.ini
COPY ./backend/app/alembic    /app/alembic

# ⬇️ NEW: copy environment file so `load_dotenv()` works inside the container
COPY ./backend/.env           /app/.env

# --- Entrypoint script ------------------------------------------------------
RUN chmod +x /app/scripts/entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/app/scripts/entrypoint.sh"]
