FROM python:3.10

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install uv (dependency manager)
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

# Set env vars
ENV PATH="/app/.venv/bin:$PATH"
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PYTHONPATH=/app

# Copy dependency files from backend folder
COPY ./backend/pyproject.toml ./backend/uv.lock ./backend/alembic.ini /app/

# Install dependencies
RUN uv sync --frozen --no-install-project

# Copy app source code from backend
COPY ./backend/app /app/app
COPY ./backend/scripts /app/scripts

# Final sync (optional but good to keep)
RUN uv sync

# Start FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
