FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY services/worker/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY services/worker/ ./worker/
COPY src/ ./src/

# Set environment variables
ENV PYTHONPATH=/app
ENV C_FORCE_ROOT=true

# Create required directories
RUN mkdir -p /app/worker/__pycache__

# Start Celery worker
CMD ["celery", "-A", "worker.tasks", "worker", "--loglevel=debug"]
