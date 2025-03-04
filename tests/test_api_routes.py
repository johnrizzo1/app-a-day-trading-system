"""Tests for API routes."""
import pytest
import pytest_asyncio
import os
import sys
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import json

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
Order = pytest.Order
Position = pytest.Position

# Import database dependency
from src.api.database import get_db

# Setup test database - use PostgreSQL instead of SQLite
SQLALCHEMY_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "postgresql://trading:trading@postgres:5432/trading_test")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables
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
@pytest_asyncio.fixture
async def test_client():
    # Create an AsyncClient with ASGITransport using our FastAPI app
    transport = ASGITransport(app=app)
    client = AsyncClient(transport=transport, base_url="http://testserver")
    
    # Yield the client for the test to use
    yield client
    
    # Close the client after the test
    # Client is automatically closed by the fixture

# We'll use this in our tests

# Session-scoped fixture to set up the database once for all tests
@pytest.fixture(scope="session")
def setup_test_db():
    # Drop and recreate all tables at the beginning of the test session
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # Create a connection
    connection = engine.connect()
    
    # Return the connection for use by other fixtures
    yield connection
    
    # Close the connection at the end of all tests
    connection.close()

# Function-scoped fixture to create a clean database state for each test
@pytest.fixture
def db_session(setup_test_db):
    # Start a transaction
    transaction = setup_test_db.begin()
    
    # Create a session bound to the transaction
    session = TestingSessionLocal(bind=setup_test_db)
    
    # Override the get_db dependency to use our test session
    def override_get_db():
        try:
            yield session
        finally:
            pass
    
    # Set the override
    original_override = app.dependency_overrides.get(get_db)
    app.dependency_overrides[get_db] = override_get_db
    
    # Set up test data within the transaction
    setup_test_db.execute(text("""
        INSERT INTO accounts (id, name, email, balance, margin_enabled, margin_ratio)
        VALUES (1, 'Test Account', 'test@example.com', 10000.00, 1, 0.1)
        ON CONFLICT (id) DO NOTHING;
    """))
    
    setup_test_db.execute(text("""
        INSERT INTO instruments (id, type, symbol, name, description, currency, is_active)
        VALUES (1, 'FUTURES', 'BTC-USD', 'Bitcoin Futures', 'Bitcoin USD Futures Contract', 'USD', 1)
        ON CONFLICT (id) DO NOTHING;
    """))
    
    # Yield the session for the test to use
    yield session
    
    # Restore the original dependency override if there was one
    if original_override:
        app.dependency_overrides[get_db] = original_override
    else:
        del app.dependency_overrides[get_db]
    
    # Close the session
    session.close()
    
    # Rollback the transaction to reset database state
    transaction.rollback()

@pytest.mark.asyncio
async def test_create_model(db_session, test_client):
    response = await test_client.post(
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
    
    # Client is automatically closed by the fixture

@pytest.mark.asyncio
async def test_create_strategy(db_session, test_client):
    
    # First create a model
    model_response = await test_client.post(
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
    response = await test_client.post(
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
    
    # Client is automatically closed by the fixture

@pytest.mark.asyncio
async def test_create_backtest(db_session, test_client):
    
    # Create model and strategy first
    model_response = await test_client.post(
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
    
    strategy_response = await test_client.post(
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
    response = await test_client.post(
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
    
    # Client is automatically closed by the fixture

@pytest.mark.asyncio
async def test_create_contract(db_session, test_client):
    
    # Create a futures contract
    expiry_date = datetime.now() + timedelta(days=60)
    response = await test_client.post(
        "/api/trading/contracts",
        json={
            "symbol": "SOL-PERP",
            "expiry": expiry_date.isoformat(),
            "tick_size": 0.001,
            "contract_size": 1.0,
            "margin_requirement": 0.05
        }
    )
    
    # Check the response
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "SOL-PERP"
    assert data["tick_size"] == 0.001
    assert data["contract_size"] == 1.0
    assert data["margin_requirement"] == 0.05
    assert "id" in data
    
    # Try to create a contract with the same symbol (should fail with 400)
    duplicate_response = await test_client.post(
        "/api/trading/contracts",
        json={
            "symbol": "SOL-PERP",
            "expiry": expiry_date.isoformat(),
            "tick_size": 0.001,
            "contract_size": 1.0,
            "margin_requirement": 0.05
        }
    )
    assert duplicate_response.status_code == 400
    
    # Client is automatically closed by the fixture

@pytest.mark.asyncio
async def test_create_order(db_session, test_client):
    
    # Create a futures contract using the API
    # This ensures the contract is created in the same database session as the order
    expiry_date = datetime.now() + timedelta(days=30)
    contract_response = await test_client.post(
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
    
    # Use the correct endpoint path and lowercase enum values
    response = await test_client.post(
        "/api/trading/orders",
        json={
            "contract_id": contract_data['id'],
            "type": "market",  # Use lowercase enum value
            "side": "buy",    # Use lowercase enum value
            "quantity": 1.0,
            "price": None,     # Optional but explicitly set to None
            "account_id": 1,   # Use the test account
            "instrument_id": 1  # Use the test instrument
        }
    )
    
    # Print the response
    print(f"\nORDER TEST - Response: {response.status_code}\n")
    if response.status_code != 200:
        print(f"Response content: {response.content}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["contract_id"] == contract_data['id']
    assert data["type"] == "market"  # API returns the enum value
    assert data["side"] == "buy"    # API returns the enum value
    assert data["quantity"] == 1.0
    
    # Client is automatically closed by the fixture

@pytest.mark.asyncio
async def test_list_orders(db_session, test_client):
    
    # First create a contract
    expiry_date = datetime.now() + timedelta(days=30)
    contract_response = await test_client.post(
        "/api/trading/contracts",
        json={
            "symbol": "ETH-PERP",
            "expiry": expiry_date.isoformat(),
            "tick_size": 0.01,
            "contract_size": 1.0,
            "margin_requirement": 0.1
        }
    )
    assert contract_response.status_code == 200
    contract_data = contract_response.json()
    
    # Create an order
    order_response = await test_client.post(
        "/api/trading/orders",
        json={
            "contract_id": contract_data['id'],
            "type": "market",
            "side": "buy",
            "quantity": 1.0,
            "price": None,
            "account_id": 1,
            "instrument_id": 1
        }
    )
    assert order_response.status_code == 200
    order_data = order_response.json()
    
    # Now test listing orders
    response = await test_client.get("/api/trading/orders")
    assert response.status_code == 200
    orders = response.json()
    assert isinstance(orders, list)
    assert len(orders) >= 1
    
    # Test filtering by contract_id
    response = await test_client.get(f"/api/trading/orders?contract_id={contract_data['id']}")
    assert response.status_code == 200
    filtered_orders = response.json()
    assert isinstance(filtered_orders, list)
    assert all(order['contract_id'] == contract_data['id'] for order in filtered_orders)
    
    # Test filtering by status
    response = await test_client.get("/api/trading/orders?status=pending")
    assert response.status_code == 200
    status_orders = response.json()
    assert isinstance(status_orders, list)
    assert all(order['status'] == 'pending' for order in status_orders)
    
    # Client is automatically closed by the fixture

@pytest.mark.asyncio
async def test_cancel_order(db_session, test_client):
    
    # First create a contract
    expiry_date = datetime.now() + timedelta(days=30)
    contract_response = await test_client.post(
        "/api/trading/contracts",
        json={
            "symbol": "LTC-PERP",
            "expiry": expiry_date.isoformat(),
            "tick_size": 0.01,
            "contract_size": 1.0,
            "margin_requirement": 0.1
        }
    )
    assert contract_response.status_code == 200
    contract_data = contract_response.json()
    
    # Create an order
    order_response = await test_client.post(
        "/api/trading/orders",
        json={
            "contract_id": contract_data['id'],
            "type": "limit",
            "side": "buy",
            "quantity": 1.0,
            "price": 100.0,
            "account_id": 1,
            "instrument_id": 1
        }
    )
    assert order_response.status_code == 200
    order_data = order_response.json()
    order_id = order_data['id']
    
    # Now cancel the order
    cancel_response = await test_client.post(f"/api/trading/orders/{order_id}/cancel")
    assert cancel_response.status_code == 200
    cancelled_order = cancel_response.json()
    assert cancelled_order['id'] == order_id
    assert cancelled_order['status'] == 'cancelled'
    
    # Try to cancel a non-existent order
    non_existent_id = 9999
    response = await test_client.post(f"/api/trading/orders/{non_existent_id}/cancel")
    assert response.status_code == 404
    
    # Client is automatically closed by the fixture

@pytest.mark.asyncio
async def test_get_positions(db_session, test_client):
    
    # Test listing positions (should be empty initially)
    response = await test_client.get("/api/trading/positions")
    assert response.status_code == 200
    positions = response.json()
    assert isinstance(positions, list)
    
    # Test filtering by contract_id (even though there are no positions)
    response = await test_client.get("/api/trading/positions?contract_id=1")
    assert response.status_code == 200
    filtered_positions = response.json()
    assert isinstance(filtered_positions, list)
    
    # Client is automatically closed by the fixture
