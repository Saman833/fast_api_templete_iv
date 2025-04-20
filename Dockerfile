FROM python:3.10

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

ENV PATH="/app/.venv/bin:$PATH"
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PYTHONPATH=/app

# Copy dependency files
COPY ./pyproject.toml ./uv.lock ./alembic.ini /app/

# Install dependencies (no cache mounts)
RUN uv sync --frozen --no-install-project

# Copy application code
COPY ./app /app/app
COPY ./scripts /app/scripts

# Final sync
RUN uv sync

# Start the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
