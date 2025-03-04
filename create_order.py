#!/usr/bin/env python3
"""Script to create an order directly using SQLAlchemy."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
sys.path.append('/app')
from src.database.models import Order, OrderType, OrderSide, OrderStatus, FuturesContract
from datetime import datetime

# Create database connection
engine = create_engine("postgresql://trading:trading@localhost:5432/trading_system")
Session = sessionmaker(bind=engine)
session = Session()

# Get the contract
contract = session.query(FuturesContract).filter_by(id=3).first()
if not contract:
    print("Contract not found")
    exit(1)

# Create an order
order = Order(
    contract_id=contract.id,
    type=OrderType.MARKET,
    side=OrderSide.BUY,
    quantity=1.0,
    price=None,
    status=OrderStatus.PENDING,
    account_id=1,
    instrument_id=1,
    created_at=datetime.utcnow(),
    updated_at=datetime.utcnow()
)

# Add and commit
session.add(order)
session.commit()
session.refresh(order)

print(f"Order created with ID: {order.id}")
print(f"Order type: {order.type}")
print(f"Order side: {order.side}")
print(f"Order status: {order.status}")
