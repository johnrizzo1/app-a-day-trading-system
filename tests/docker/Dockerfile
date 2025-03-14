FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including Node.js
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g yarn \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY services/api/requirements.txt api-requirements.txt
COPY requirements.txt root-requirements.txt
RUN pip install --no-cache-dir -r api-requirements.txt -r root-requirements.txt pytest-cov httpx pytest-asyncio

# Create a simple directory structure for testing
RUN mkdir -p /app/src/database/models
RUN mkdir -p /app/ui

# Copy application code
COPY services/api/ ./api/
COPY src/ ./src/
COPY tests/ ./tests/
COPY pytest.ini ./pytest.ini

# Set environment variables
ENV PYTHONPATH=/app:/app/services
ENV TEST_DATABASE_URL=postgresql://trading:trading@postgres:5432/trading_test
ENV NODE_ENV=test

# Create a script to run backend tests with proper imports
RUN echo '#!/bin/bash\n\
echo "Running backend tests..."\n\
python -c "\n\
import sys\n\
from pathlib import Path\n\
\n\
# Ensure the src directory is in the Python path\n\
sys.path.insert(0, str(Path(\".\").absolute()))\n\
\n\
# Create a simple __init__.py file in the models directory if it doesn't exist\n\
models_init = Path(\"src/database/models/__init__.py\")\n\
if not models_init.exists() or models_init.stat().st_size == 0:\n\
    with open(models_init, \"w\") as f:\n\
        f.write(\"# Auto-generated by test setup\\n\")\n\
"\n\
pytest "$@"' > /app/run_backend_tests.sh && chmod +x /app/run_backend_tests.sh

# Create a script to run UI tests
RUN echo '#!/bin/bash\n\
echo "Running UI tests..."\n\
cd /app/ui\n\
if [ -f "package.json" ]; then\n\
  # Install dependencies if not already installed\n\
  echo "Installing UI dependencies..."\n\
  yarn install\n\
  # Install Jest globally to ensure it is available\n\
  npm install -g jest\n\
\n\
  # Run tests for all packages with tests\n\
  for pkg in packages/*/; do\n\
    if [ -d "${pkg}__tests__" ] || [ -d "${pkg}tests" ]; then\n\
      echo "Running tests for ${pkg}..."\n\
      cd /app/ui/${pkg}\n\
      # Install package dependencies\n\
      if [ -f "package.json" ]; then\n\
        echo "Installing package dependencies for ${pkg}..."\n\
        yarn install\n\
        # Verify that all testing dependencies are installed\n\
        if ! yarn list --depth=0 | grep -q "@testing-library/dom"; then\n\
          echo "Installing missing testing dependencies..."\n\
          yarn add --dev @testing-library/dom @testing-library/jest-dom @testing-library/react @testing-library/user-event\n\
        fi\n\
      fi\n\
      # Set NODE_PATH to include all possible node_modules locations\n\
      export NODE_PATH=/app/ui/node_modules:/app/ui/${pkg}node_modules:$NODE_PATH\n\
      # Use npx to run the locally installed jest\n\
      if [ -f "node_modules/.bin/jest" ]; then\n\
        echo "Running tests with local jest..."\n\
        ./node_modules/.bin/jest "$@"\n\
      else\n\
        echo "Running tests with yarn test..."\n\
        yarn test "$@"\n\
      fi\n\
      TEST_EXIT=$?\n\
      if [ $TEST_EXIT -ne 0 ]; then\n\
        echo "Tests failed for ${pkg}"\n\
        exit $TEST_EXIT\n\
      fi\n\
      cd /app/ui\n\
    fi\n\
  done\n\
else\n\
  echo "No UI package.json found. Skipping UI tests."\n\
fi' > /app/run_ui_tests.sh && chmod +x /app/run_ui_tests.sh

# Create a combined test script
RUN echo '#!/bin/bash\n\
# Run backend tests first\n\
/app/run_backend_tests.sh "$@"\n\
BACKEND_EXIT=$?\n\
\n\
# Run UI tests\n\
/app/run_ui_tests.sh\n\
UI_EXIT=$?\n\
\n\
# Return non-zero exit code if either test suite failed\n\
if [ $BACKEND_EXIT -ne 0 ] || [ $UI_EXIT -ne 0 ]; then\n\
  exit 1\n\
fi\n\
\n\
exit 0' > /app/run_all_tests.sh && chmod +x /app/run_all_tests.sh

# Default command to run all tests
CMD ["/app/run_all_tests.sh"]
