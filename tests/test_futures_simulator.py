"""Tests for the futures market simulator."""
import pytest
from datetime import datetime, timedelta
import numpy as np
from services.market_simulator.futures_simulator import FuturesContract, FuturesSimulator

@pytest.fixture
def simulator():
    return FuturesSimulator("redis://localhost:6379")

def test_futures_contract_initialization():
    expiry = datetime.now() + timedelta(days=30)
    contract = FuturesContract(
        symbol="BTC-PERP",
        expiry=expiry,
        initial_price=50000.0,
        tick_size=0.1,
        contract_size=1.0
    )
    
    assert contract.symbol == "BTC-PERP"
    assert contract.expiry == expiry
    assert contract.price == 50000.0
    assert contract.tick_size == 0.1
    assert contract.contract_size == 1.0
    assert isinstance(contract.funding_rate, float)

def test_contract_to_dict():
    expiry = datetime.now() + timedelta(days=30)
    contract = FuturesContract(
        symbol="ETH-PERP",
        expiry=expiry,
        initial_price=3000.0,
        tick_size=0.1,
        contract_size=1.0
    )
    
    contract_dict = contract.to_dict()
    assert contract_dict["symbol"] == "ETH-PERP"
    assert contract_dict["expiry"] == expiry.isoformat()
    assert contract_dict["price"] == 3000.0
    assert contract_dict["tick_size"] == 0.1
    assert contract_dict["contract_size"] == 1.0
    assert isinstance(contract_dict["funding_rate"], float)

def test_simulator_initialization(simulator):
    assert len(simulator.contracts) > 0
    assert any("-PERP" in symbol for symbol in simulator.contracts.keys())

def test_price_impact_calculation(simulator):
    base_price = 50000.0
    volume = 100.0
    impact_price = simulator._calculate_price_impact(base_price, volume)
    assert impact_price > base_price

def test_funding_rate_updates(simulator):
    # Get a perpetual contract
    perp_contract = next(c for c in simulator.contracts.values() if "-PERP" in c.symbol)
    
    # Store initial funding rate
    initial_rate = perp_contract.funding_rate
    
    # Force funding rate update by setting last_funding to old time
    perp_contract.last_funding = datetime.now() - timedelta(hours=9)
    simulator._update_funding_rates()
    
    assert perp_contract.funding_rate != initial_rate

def test_price_updates(simulator):
    updates = simulator.generate_price_updates()
    
    assert len(updates) == len(simulator.contracts)
    for update in updates:
        assert "contract" in update
        assert "timestamp" in update
        assert "volume" in update
        assert "open_interest" in update
        
        contract_data = update["contract"]
        assert "symbol" in contract_data
        assert "price" in contract_data
        assert "tick_size" in contract_data
        
        # Verify price is multiple of tick size
        price = contract_data["price"]
        tick_size = contract_data["tick_size"]
        assert abs(price / tick_size - round(price / tick_size)) < 1e-10
