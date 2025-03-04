"""Celery tasks for handling trading operations."""
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = str(Path(__file__).resolve().parents[2])
if project_root not in sys.path:
    sys.path.append(project_root)

from celery import Celery
from sqlalchemy.orm import Session
from typing import Dict, Any
import logging
from redis import Redis
import json
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Initialize Celery
celery = Celery('worker.tasks')
celery.conf.update(
    broker_url='redis://redis:6379/0',
    result_backend='redis://redis:6379/0',
    imports=['worker.tasks'],
    task_serializer='json',
    result_serializer='json',
    accept_content=['json']
)

# Import models after Celery configuration to avoid circular imports
from src.database.models.order import Order, Trade
from src.database.models.account import Position
from src.database.models.base import OrderStatus, InstrumentType, Instrument
from src.database.models.instrument import Equity, Bond, FuturesContract
from src.database.session import get_db

@celery.task
def execute_order(order_id: int) -> Dict[str, Any]:
    """Execute a trade order."""
    db = next(get_db())
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise ValueError(f"Order {order_id} not found")
        
        # Check if order is already processed
        if order.status != OrderStatus.PENDING:
            return {"status": "skipped", "reason": f"Order already {order.status}"}
            
        # Get current market price from Redis
        redis_client = Redis(host='redis', port=6379, db=0)
        market_data = redis_client.get(f"quote:{order.instrument.symbol}")
        if not market_data:
            raise ValueError(f"No market data for {order.instrument.symbol}")
            
        market_data = json.loads(market_data)
        current_price = float(market_data['price'])
        
        # Check if limit order conditions are met
        if order.type == OrderType.LIMIT:
            if order.side == OrderSide.BUY and current_price > order.price:
                return {"status": "pending", "reason": "Price above limit"}
            if order.side == OrderSide.SELL and current_price < order.price:
                return {"status": "pending", "reason": "Price below limit"}
        
        # Execute trade
        trade = Trade(
            order_id=order.id,
            instrument_id=order.instrument_id,
            price=current_price,
            quantity=order.quantity,
            side=order.side
        )
        db.add(trade)
        
        # Update position
        position = db.query(Position).filter(
            Position.instrument_id == order.instrument_id,
            Position.account_id == order.account_id
        ).first()
        
        if not position:
            position = Position(
                instrument_id=order.instrument_id,
                account_id=order.account_id,
                quantity=0
            )
            db.add(position)
        
        # Update position quantity
        if order.side == OrderSide.BUY:
            position.quantity += order.quantity
        else:
            position.quantity -= order.quantity
        
        # Update order status
        order.status = OrderStatus.FILLED
        order.filled_price = current_price
        order.filled_at = datetime.utcnow()
        
        db.commit()
        
        return {
            "status": "success",
            "trade_id": trade.id,
            "filled_price": current_price
        }
        
    except Exception as e:
        logger.error(f"Error executing order {order_id}: {str(e)}")
        db.rollback()
        
        # Update order status to rejected
        try:
            order.status = OrderStatus.REJECTED
            order.rejection_reason = str(e)
            db.commit()
        except:
            pass
            
        return {"status": "error", "error": str(e)}
    finally:
        db.close()

@celery.task
def process_corporate_actions():
    """Process corporate actions for equities (dividends, splits, etc)."""
    db = next(get_db())
    try:
        # Get all active equity positions
        positions = db.query(Position).join(
            Instrument
        ).filter(
            Instrument.type == InstrumentType.EQUITY,
            Position.quantity > 0
        ).all()
        
        for position in positions:
            equity = position.instrument
            
            # Process dividends
            if equity.next_dividend_date and equity.next_dividend_date.date() == datetime.utcnow().date():
                dividend_amount = position.quantity * equity.dividend_per_share
                
                # Create dividend payment record
                payment = DividendPayment(
                    position_id=position.id,
                    amount=dividend_amount,
                    payment_date=datetime.utcnow()
                )
                db.add(payment)
                
                # Update account balance
                position.account.balance += dividend_amount
                
                # Update next dividend date
                equity.next_dividend_date += timedelta(days=90)  # Assuming quarterly dividends
                
        db.commit()
        return {"status": "success"}
        
    except Exception as e:
        logger.error(f"Error processing corporate actions: {str(e)}")
        db.rollback()
        return {"status": "error", "error": str(e)}
    finally:
        db.close()

@celery.task
def calculate_portfolio_metrics(account_id: int):
    """Calculate portfolio metrics for an account."""
    db = next(get_db())
    try:
        positions = db.query(Position).filter(
            Position.account_id == account_id,
            Position.quantity != 0
        ).all()
        
        total_value = 0
        portfolio_beta = 0
        asset_allocation = {
            InstrumentType.EQUITY: 0,
            InstrumentType.BOND: 0,
            InstrumentType.FUTURES: 0
        }
        
        for position in positions:
            instrument = position.instrument
            current_value = position.quantity * float(instrument.last_price)
            total_value += current_value
            
            # Track asset allocation
            asset_allocation[instrument.type] += current_value
            
            # Calculate portfolio beta (for equities)
            if instrument.type == InstrumentType.EQUITY:
                portfolio_beta += (current_value / total_value) * instrument.beta
        
        # Convert asset allocation to percentages
        for asset_type in asset_allocation:
            asset_allocation[asset_type] = (
                asset_allocation[asset_type] / total_value * 100
                if total_value > 0 else 0
            )
        
        # Store metrics
        metrics = PortfolioMetrics(
            account_id=account_id,
            total_value=total_value,
            portfolio_beta=portfolio_beta,
            equity_allocation=asset_allocation[InstrumentType.EQUITY],
            bond_allocation=asset_allocation[InstrumentType.BOND],
            futures_allocation=asset_allocation[InstrumentType.FUTURES],
            timestamp=datetime.utcnow()
        )
        db.add(metrics)
        db.commit()
        
        return {
            "status": "success",
            "metrics": {
                "total_value": total_value,
                "portfolio_beta": portfolio_beta,
                "asset_allocation": asset_allocation
            }
        }
        
    except Exception as e:
        logger.error(f"Error calculating portfolio metrics: {str(e)}")
        db.rollback()
        return {"status": "error", "error": str(e)}
    finally:
        db.close()
