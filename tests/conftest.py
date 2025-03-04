"""Pytest configuration file."""
import sys
import os
import pytest
import pytest_asyncio

# Configure pytest-asyncio using the proper method
# This will be handled by pytest.ini or pyproject.toml

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the models directly for testing
# Use a direct import to avoid issues with __init__.py
import sys
import importlib.util
import os

# Directly import the models.py file
models_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'database', 'models.py')
spec = importlib.util.spec_from_file_location('models_module', models_path)
models_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(models_module)

# Get the models from the imported module
Base = models_module.Base
FinancialModel = models_module.FinancialModel
Strategy = models_module.Strategy
Backtest = models_module.Backtest
FuturesContract = models_module.FuturesContract
Position = models_module.Position
Order = models_module.Order
Account = models_module.Account
Instrument = models_module.Instrument

# Make them available to all test modules
pytest.Base = Base
pytest.FinancialModel = FinancialModel
pytest.Strategy = Strategy
pytest.Backtest = Backtest
pytest.FuturesContract = FuturesContract
pytest.Position = Position
pytest.Order = Order
pytest.Account = Account
pytest.Instrument = Instrument
