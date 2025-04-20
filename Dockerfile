FROM python:3.10

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install uv (dependency manager)
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

# Add uv binary to path
ENV PATH="/app/.venv/bin:$PATH"
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PYTHONPATH=/app

# Copy requirement files early
COPY ./pyproject.toml ./uv.lock ./alembic.ini /app/

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

# Copy app code
COPY ./app /app/app
COPY ./scripts /app/scripts

# Install project itself (optional)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

# Run FastAPI via uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
