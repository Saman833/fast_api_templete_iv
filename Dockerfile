# ──────────────────────────────
#  Dockerfile – FastAPI backend
#  with Alembic auto-migration
# ──────────────────────────────
FROM python:3.10-slim

# ---------------------------------------------------------------------------
# Basic runtime settings
# ---------------------------------------------------------------------------
ENV PYTHONUNBUFFERED=1      \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# ---------------------------------------------------------------------------
# Paths & environment
# ---------------------------------------------------------------------------
ENV VENV_PATH="/app/.venv"
ENV PATH="$VENV_PATH/bin:$PATH"
ENV PYTHONPATH="/app"

# ---------------------------------------------------------------------------
# System dependencies (build-essential, libpq for PostgreSQL, etc.)
# ---------------------------------------------------------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        libpq-dev \
        curl && \
    rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------------------------------
# Virtual environment
# ---------------------------------------------------------------------------
RUN python -m venv "${VENV_PATH}"

# ---------------------------------------------------------------------------
# Python requirements
# ---------------------------------------------------------------------------
COPY ./backend/requirements.txt /app/requirements.txt

RUN "${VENV_PATH}/bin/pip" install --upgrade pip && \
    "${VENV_PATH}/bin/pip" install -r /app/requirements.txt

# ---------------------------------------------------------------------------
# Application source
# ---------------------------------------------------------------------------
COPY ./backend/app      /app/app
COPY ./backend/scripts  /app/scripts

# Make the entry-point script executable
RUN chmod +x /app/scripts/entrypoint.sh

# ---------------------------------------------------------------------------
# Network / runtime
# ---------------------------------------------------------------------------
EXPOSE 8000

# Use the script that:
#   1. Activates the venv
#   2. Generates an Alembic revision (autogenerate) if needed
#   3. Upgrades to head
#   4. Launches Uvicorn
ENTRYPOINT ["/app/scripts/entrypoint.sh"]
