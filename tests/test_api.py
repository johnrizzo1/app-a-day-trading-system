#!/usr/bin/env python3
"""Tests for the API endpoints."""
import http.client
import json
import random
import string
import pytest
from datetime import datetime


def generate_unique_symbol():
    """Generate a unique symbol for testing."""
    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    current_date = datetime.now().strftime("%Y%m%d")
    return f"TEST-{current_date}-{random_suffix}"


def test_create_contract_and_order():
    """Test creating a contract and an order."""
    # Create a contract with a unique symbol
    unique_symbol = generate_unique_symbol()
    contract_data = {
        "symbol": unique_symbol,
        "expiry": "2025-12-31",
        "tick_size": 0.01,
        "contract_size": 1.0,
        "margin_requirement": 0.1
    }
    
    print(f"Creating contract with symbol: {unique_symbol}")
    
    try:
        # Connect to the API
        conn = http.client.HTTPConnection("localhost", 8000)
        
        # Send the contract creation request
        headers = {"Content-Type": "application/json"}
        conn.request("POST", "/api/trading/contracts", body=json.dumps(contract_data), headers=headers)
        
        # Get the response
        response = conn.getresponse()
        response_data = response.read().decode()
        
        print("Contract creation response:")
        print(f"Status: {response.status}")
        print(response_data)
        
        # Parse the response to get the contract ID
        contract_response = json.loads(response_data)
        
        # Assert contract creation was successful
        assert response.status in [200, 201], f"Failed to create contract: {response_data}"
        assert "id" in contract_response, "Contract response does not contain an ID"
        
        contract_id = contract_response["id"]
        
        # Create an order
        order_data = {
            "contract_id": contract_id,
            "type": "market",
            "side": "buy",
            "quantity": 1.0,
            "price": None,
            "account_id": 1
        }
        
        # Send the order creation request
        conn.request("POST", "/api/trading/orders", body=json.dumps(order_data), headers=headers)
        
        # Get the response
        response = conn.getresponse()
        response_data = response.read().decode()
        
        print("\nOrder creation response:")
        print(f"Status: {response.status}")
        print(response_data)
        
        # Assert order creation was successful
        assert response.status in [200, 201], f"Failed to create order: {response_data}"
        order_response = json.loads(response_data)
        assert "id" in order_response, "Order response does not contain an ID"
        
        # Close the connection
        conn.close()
        
    except ConnectionRefusedError:
        pytest.skip("API server is not running. Start with docker-compose up -d")
    except Exception as e:
        pytest.fail(f"Unexpected error: {type(e).__name__}: {e}")


# This allows the script to be run directly
if __name__ == "__main__":
    try:
        test_create_contract_and_order()
        print("\nTest completed successfully!")
    except ConnectionRefusedError:
        print("\nERROR: Connection refused. Make sure the API server is running.")
        print("Check if the Docker container is running with: docker-compose ps")
        print("Start the services with: docker-compose up -d")
    except Exception as e:
        print(f"\nERROR: {type(e).__name__}: {e}")
