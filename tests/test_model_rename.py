"""Test to verify the Model class has been renamed to FinancialModel."""
import sys
import os
import pytest

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the models directly
import importlib.util
import os

# Directly import the models.py file
models_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'database', 'models.py')
spec = importlib.util.spec_from_file_location('models_module', models_path)
models_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(models_module)

# Get the models from the imported module
FinancialModel = models_module.FinancialModel
Strategy = models_module.Strategy

def test_financial_model_exists():
    """Test that FinancialModel class exists."""
    assert FinancialModel.__name__ == "FinancialModel"
    assert FinancialModel.__tablename__ == "models"

def test_strategy_uses_financial_model():
    """Test that Strategy class uses FinancialModel."""
    # Check the relationship attribute
    assert Strategy.model.property.mapper.class_.__name__ == "FinancialModel"
