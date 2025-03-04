#!/usr/bin/env bash
set -e

# Initialize environment
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
fi

# Initialize Python virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
yarn install

# Initialize database
echo "Setting up database..."
docker-compose up -d postgres redis

echo "Setup complete! You can now start the development server with:"
echo "devenv up"
