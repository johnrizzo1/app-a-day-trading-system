FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY services/market_simulator/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY services/market_simulator/ ./services/market_simulator/
COPY src/ ./src/

# Set environment variables
ENV PYTHONPATH=/app

# Start market simulator
CMD ["python", "-m", "services.market_simulator"]
