"""API endpoints for instrument trading."""
from fastapi import APIRouter, HTTPException, Depends, WebSocket
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
import redis
from ..database import get_db
from ...database.models import (
    Instrument, Equity, Bond, Position, Order,
    OrderType, OrderSide, OrderStatus, InstrumentType
)

router = APIRouter(prefix="/api/instruments", tags=["instruments"])

class InstrumentResponse(BaseModel):
    id: int
    type: InstrumentType
    symbol: str
    name: str
    
    model_config = ConfigDict(from_attributes=True)

class EquityResponse(InstrumentResponse):
    exchange: str
    sector: str
    market_cap: float
    shares_outstanding: float
    dividend_yield: Optional[float]

class BondResponse(InstrumentResponse):
    issuer: str
    maturity_date: datetime
    coupon_rate: float
    face_value: float
    payment_frequency: int
    credit_rating: str

@router.get("/equities", response_model=List[EquityResponse])
async def list_equities(
    sector: Optional[str] = None,
    min_market_cap: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """List available equity instruments."""
    query = db.query(Equity)
    if sector:
        query = query.filter(Equity.sector == sector)
    if min_market_cap:
        query = query.filter(Equity.market_cap >= min_market_cap)
    return query.all()

@router.get("/bonds", response_model=List[BondResponse])
async def list_bonds(
    min_rating: Optional[str] = None,
    max_maturity: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """List available bond instruments."""
    query = db.query(Bond)
    if min_rating:
        query = query.filter(Bond.credit_rating <= min_rating)  # 'AAA' < 'BB'
    if max_maturity:
        query = query.filter(Bond.maturity_date <= max_maturity)
    return query.all()

@router.get("/{instrument_id}/quote")
async def get_quote(instrument_id: int, db: Session = Depends(get_db)):
    """Get current quote for an instrument."""
    instrument = db.query(Instrument).filter(Instrument.id == instrument_id).first()
    if not instrument:
        raise HTTPException(status_code=404, detail="Instrument not found")
    
    redis_client = redis.from_url('redis://redis:6379')
    quote_data = redis_client.get(f"quote:{instrument.symbol}")
    
    if not quote_data:
        raise HTTPException(status_code=404, detail="Quote not available")
    
    return json.loads(quote_data)

@router.websocket("/market-data/{instrument_type}")
async def market_data_websocket(
    websocket: WebSocket,
    instrument_type: InstrumentType
):
    """WebSocket endpoint for real-time market data."""
    await websocket.accept()
    redis_client = redis.from_url('redis://redis:6379')
    pubsub = redis_client.pubsub()
    
    # Subscribe to appropriate channel based on instrument type
    channel = f"market_data:{instrument_type.value}"
    pubsub.subscribe(channel)
    
    try:
        for message in pubsub.listen():
            if message['type'] == 'message':
                await websocket.send_text(message['data'].decode('utf-8'))
    except Exception:
        await websocket.close()
    finally:
        pubsub.unsubscribe(channel)

@router.post("/{instrument_id}/orders")
async def place_order(
    instrument_id: int,
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    """Place an order for any instrument type."""
    instrument = db.query(Instrument).filter(Instrument.id == instrument_id).first()
    if not instrument:
        raise HTTPException(status_code=404, detail="Instrument not found")
    
    # Validate order based on instrument type
    if isinstance(instrument, Bond):
        if order.quantity % 1 != 0:  # Bonds typically trade in whole units
            raise HTTPException(
                status_code=400,
                detail="Bond orders must be in whole units"
            )
    
    # Create and execute order
    db_order = Order(
        instrument_id=instrument_id,
        order_type=order.order_type,
        side=order.side,
        quantity=order.quantity,
        price=order.price
    )
    
    db.add(db_order)
    try:
        db.commit()
        db.refresh(db_order)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
    # Execute order (async)
    background_tasks.add_task(execute_order, db_order.id)
    return db_order
