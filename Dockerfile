FROM python:3.10

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Set env vars
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app

# Create virtual environment
RUN python -m venv /app/.venv

# Copy requirements file
COPY ./backend/requirements.txt /app/

# Install dependencies
RUN /app/.venv/bin/pip install --upgrade pip && /app/.venv/bin/pip install -r requirements.txt

# Copy app source code from backend
COPY ./backend/app /app/app
COPY ./backend/scripts /app/scripts

# Start FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
