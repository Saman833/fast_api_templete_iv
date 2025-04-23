FROM python:3.10-slim

# Disable .pyc generation and enable unbuffered logs
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

# Set environment variables
ENV VENV_PATH="/app/.venv"
ENV PATH="$VENV_PATH/bin:$PATH"
ENV PYTHONPATH="/app"

# Install system packages (required by some Python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtualenv
RUN python -m venv $VENV_PATH

# Copy and inspect requirements.txt
COPY ./backend/requirements.txt /app/
RUN cat /app/requirements.txt

# Install dependencies with pip directly from the venv
RUN $VENV_PATH/bin/pip install --upgrade pip
RUN $VENV_PATH/bin/pip install -r /app/requirements.txt

# Copy app source code
COPY ./backend/app /app/app
COPY ./backend/scripts /app/scripts

# Expose port for FastAPI
EXPOSE 8000

# Start FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
