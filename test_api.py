#!/usr/bin/env python3
"""Script to test the API directly."""
import http.client
import json

# Create a contract
contract_data = {
    "symbol": "ETH-USD",
    "expiry": "2025-12-31",
    "tick_size": 0.01,
    "contract_size": 1.0,
    "margin_requirement": 0.1
}

# Connect to the API
conn = http.client.HTTPConnection("localhost", 8000)

# Send the contract creation request
headers = {"Content-Type": "application/json"}
conn.request("POST", "/api/trading/contracts", body=json.dumps(contract_data), headers=headers)

# Get the response
response = conn.getresponse()
response_data = response.read().decode()

print("Contract creation response:")
print(response.status)
print(response_data)

# Parse the response to get the contract ID
contract_response = json.loads(response_data)
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
print(response.status)
print(response_data)

# Close the connection
conn.close()
