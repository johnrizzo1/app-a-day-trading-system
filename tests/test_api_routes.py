"""Tests for API routes."""
import pytest
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

# Ensure the path is set up correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  

import pytest
from src.api.main import app

# Get models from pytest fixtures (defined in conftest.py)
Base = pytest.Base
Model = pytest.Model
Strategy = pytest.Strategy
Backtest = pytest.Backtest
FuturesContract = pytest.FuturesContract

# Import database dependency
from src.api.database import get_db

# Setup test database - use PostgreSQL instead of SQLite
SQLALCHEMY_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "postgresql://trading:trading@postgres:5432/trading_test")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Use the HTTPX AsyncClient with ASGITransport for FastAPI testing
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport

# Create a test client for FastAPI app
async def get_test_client():
    # Create an AsyncClient with ASGITransport using our FastAPI app
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://testserver")

# We'll use this in our tests

@pytest.fixture
def db_session():
    # Drop and recreate all tables before starting the test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # Create a connection and start a transaction
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    # Close session and rollback transaction after the test
    session.close()
    transaction.rollback()
    connection.close()

@pytest.mark.asyncio
async def test_create_model(db_session):
    client = await get_test_client()
    response = await client.post(
        "/api/models/",
        json={
            "name": "Test Model",
            "description": "Test Description",
            "parameters": {"param1": "value1"}
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Model"
    assert data["description"] == "Test Description"
    assert data["parameters"] == {"param1": "value1"}
    
    await client.aclose()

@pytest.mark.asyncio
async def test_create_strategy(db_session):
    client = await get_test_client()
    
    # First create a model
    model_response = await client.post(
        "/api/models/",
        json={
            "name": "Test Model for Strategy",
            "description": "Test Description",
            "parameters": {"param1": "value1"}
        }
    )
    # Print the response to debug
    print("Model Response:", model_response.json())
    
    # Get the model ID from the response
    model_data = model_response.json()
    assert "id" in model_data, f"Model response missing 'id' field: {model_data}"
    model_id = model_data["id"]
    
    # Create strategy
    response = await client.post(
        "/api/strategies/",
        json={
            "name": "Test Strategy",
            "model_id": model_id,
            "parameters": {"param1": "value1"}
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Strategy"
    assert data["model_id"] == model_id
    
    await client.aclose()

@pytest.mark.asyncio
async def test_create_backtest(db_session):
    client = await get_test_client()
    
    # Create model and strategy first
    model_response = await client.post(
        "/api/models/",
        json={
            "name": "Test Model for Backtest",
            "description": "Test Description",
            "parameters": {"param1": "value1"}
        }
    )
    # Print the response to debug
    model_data = model_response.json()
    print(f"\nBACKTEST TEST - Model Response: {model_data}\n")
    
    # Get the model ID from the response
    assert "id" in model_data, f"Model response missing 'id' field: {model_data}"
    model_id = model_data["id"]
    
    strategy_response = await client.post(
        "/api/strategies/",
        json={
            "name": "Test Strategy for Backtest",
            "model_id": model_id,
            "parameters": {"param1": "value1"}
        }
    )
    
    # Print the strategy response
    strategy_data = strategy_response.json()
    print(f"\nBACKTEST TEST - Strategy Response: {strategy_data}\n")
    
    # Get the strategy ID
    assert "id" in strategy_data, f"Strategy response missing 'id' field: {strategy_data}"
    strategy_id = strategy_data["id"]
    
    # Create backtest
    response = await client.post(
        "/api/backtests/",
        json={
            "strategy_id": strategy_id,
            "start_date": datetime.now().isoformat(),
            "end_date": (datetime.now() + timedelta(days=1)).isoformat(),
            "initial_capital": 10000.0
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["strategy_id"] == strategy_id
    assert data["initial_capital"] == 10000.0
    
    await client.aclose()

@pytest.mark.asyncio
async def test_create_order(db_session):
    client = await get_test_client()
    
    # Create a futures contract using the API
    # This ensures the contract is created in the same database session as the order
    expiry_date = datetime.now() + timedelta(days=30)
    contract_response = await client.post(
        "/api/trading/contracts",
        json={
            "symbol": "BTC-PERP",
            "expiry": expiry_date.isoformat(),
            "tick_size": 0.1,
            "contract_size": 1.0,
            "margin_requirement": 0.1
        }
    )
    
    # Check that the contract was created successfully
    assert contract_response.status_code == 200, f"Failed to create contract: {contract_response.content}"
    contract_data = contract_response.json()
    
    # Print the contract ID
    print(f"\nORDER TEST - Contract Response: {contract_data}\n")
    print(f"\nORDER TEST - Contract ID: {contract_data['id']}\n")
    
    # Use the correct endpoint path and enum names from the model
    response = await client.post(
        "/api/trading/orders",  # This matches the endpoint in main.py
        json={
            "contract_id": contract_data['id'],
            "order_type": "MARKET",  # Use the enum name, not the value
            "side": "BUY",  # Use the enum name, not the value
            "quantity": 1.0,
            "price": None  # Optional but explicitly set to None
        }
    )
    
    # Print the response
    print(f"\nORDER TEST - Response: {response.status_code}\n")
    if response.status_code != 200:
        print(f"Response content: {response.content}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["contract_id"] == contract_data['id']
    assert data["order_type"] == "market"  # API returns the enum value, not the name
    assert data["side"] == "buy"  # API returns the enum value, not the name
    assert data["quantity"] == 1.0
    
    await client.aclose()

@pytest.mark.asyncio
async def test_get_positions(db_session):
    client = await get_test_client()
    
    response = await client.get("/api/trading/positions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
    await client.aclose()
