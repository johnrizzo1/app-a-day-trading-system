"""Trading API endpoints."""
from fastapi import APIRouter, HTTPException, Depends, WebSocket
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import json
import redis
from ..database import get_db
from ...database.models import Order, OrderType, OrderSide, OrderStatus, Position, FuturesContract

router = APIRouter(prefix="/api/trading", tags=["trading"])

class OrderCreate(BaseModel):
    contract_id: int
    order_type: OrderType
    side: OrderSide
    quantity: float
    price: Optional[float] = None

class OrderResponse(BaseModel):
    id: int
    contract_id: int
    order_type: OrderType
    side: OrderSide
    quantity: float
    price: Optional[float]
    status: OrderStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class PositionResponse(BaseModel):
    id: int
    contract_id: int
    quantity: float
    entry_price: float
    current_price: float
    unrealized_pnl: float
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

@router.post("/orders", response_model=OrderResponse)
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    # Verify contract exists
    contract = db.query(FuturesContract).filter(FuturesContract.id == order.contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    # Validate order
    if order.order_type != OrderType.MARKET and not order.price:
        raise HTTPException(status_code=400, detail="Price required for limit/stop orders")
    
    db_order = Order(**order.dict())
    db.add(db_order)
    try:
        db.commit()
        db.refresh(db_order)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return db_order

@router.get("/orders", response_model=List[OrderResponse])
async def list_orders(
    status: Optional[OrderStatus] = None,
    contract_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Order)
    if status:
        query = query.filter(Order.status == status)
    if contract_id:
        query = query.filter(Order.contract_id == contract_id)
    return query.all()

@router.post("/orders/{order_id}/cancel", response_model=OrderResponse)
async def cancel_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.status != OrderStatus.PENDING:
        raise HTTPException(status_code=400, detail="Can only cancel pending orders")
    
    order.status = OrderStatus.CANCELLED
    try:
        db.commit()
        db.refresh(order)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return order

@router.get("/positions", response_model=List[PositionResponse])
async def list_positions(
    contract_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Position)
    if contract_id:
        query = query.filter(Position.contract_id == contract_id)
    return query.all()

@router.websocket("/market-data")
async def market_data_websocket(websocket: WebSocket):
    await websocket.accept()
    redis_client = redis.from_url('redis://redis:6379')
    pubsub = redis_client.pubsub()
    pubsub.subscribe('futures_market_data')
    
    try:
        for message in pubsub.listen():
            if message['type'] == 'message':
                await websocket.send_text(message['data'].decode('utf-8'))
    except Exception:
        await websocket.close()
    finally:
        pubsub.unsubscribe('futures_market_data')
