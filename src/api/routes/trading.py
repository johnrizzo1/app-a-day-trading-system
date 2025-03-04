"""Trading API endpoints."""
from fastapi import APIRouter, HTTPException, Depends, WebSocket
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime
import json
import redis
from ..database import get_db
# Direct import from models.py to avoid circular imports
import importlib.util
import os

# Directly import the models.py file
models_path = os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'models.py')
spec = importlib.util.spec_from_file_location('models_module', models_path)
models_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(models_module)

# Get the models from the imported module
Order = models_module.Order
OrderType = models_module.OrderType
OrderSide = models_module.OrderSide
OrderStatus = models_module.OrderStatus
Position = models_module.Position
FuturesContract = models_module.FuturesContract

router = APIRouter(prefix="/api/trading", tags=["trading"])

class ContractCreate(BaseModel):
    symbol: str
    expiry: datetime
    tick_size: float
    contract_size: float
    margin_requirement: float

class OrderCreate(BaseModel):
    contract_id: int
    type: OrderType
    side: OrderSide
    quantity: float
    price: Optional[float] = None
    # These are required by the database schema but we'll set default values
    account_id: int = 1  # Default account
    instrument_id: int = 1  # Default instrument
    
    # Add validators to handle both uppercase and lowercase enum values
    @field_validator('type', mode='before')
    @classmethod
    def validate_type(cls, v):
        if isinstance(v, str):
            try:
                return OrderType[v.upper()]
            except KeyError:
                pass
        return v
    
    @field_validator('side', mode='before')
    @classmethod
    def validate_side(cls, v):
        if isinstance(v, str):
            try:
                return OrderSide[v.upper()]
            except KeyError:
                pass
        return v

class OrderResponse(BaseModel):
    id: int
    contract_id: int
    type: OrderType
    side: OrderSide
    quantity: float
    price: Optional[float]
    status: OrderStatus
    created_at: datetime
    updated_at: datetime
    account_id: int
    instrument_id: int
    filled_quantity: Optional[float]

    model_config = ConfigDict(from_attributes=True)

class ContractResponse(BaseModel):
    id: int
    symbol: str
    expiry: datetime
    tick_size: float
    contract_size: float
    margin_requirement: float
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PositionResponse(BaseModel):
    id: int
    contract_id: int
    quantity: float
    entry_price: float
    current_price: float
    unrealized_pnl: float
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

@router.post("/contracts", response_model=ContractResponse)
async def create_contract(contract: ContractCreate, db: Session = Depends(get_db)):
    # Check if contract with same symbol already exists
    existing_contract = db.query(FuturesContract).filter(FuturesContract.symbol == contract.symbol).first()
    if existing_contract:
        raise HTTPException(status_code=400, detail="Contract with this symbol already exists")
    
    # Create the contract
    db_contract = FuturesContract(
        symbol=contract.symbol,
        expiry=contract.expiry,
        tick_size=contract.tick_size,
        contract_size=contract.contract_size,
        margin_requirement=contract.margin_requirement
    )
    db.add(db_contract)
    try:
        db.commit()
        db.refresh(db_contract)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return db_contract

@router.post("/orders", response_model=OrderResponse)
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    # Verify contract exists
    contract = db.query(FuturesContract).filter(FuturesContract.id == order.contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    # Validate order
    if order.type != OrderType.MARKET and not order.price:
        raise HTTPException(status_code=400, detail="Price required for limit/stop orders")
    
    # Create the order
    db_order = Order(
        contract_id=order.contract_id,
        type=order.type,
        side=order.side,
        quantity=order.quantity,
        price=order.price,
        account_id=order.account_id,
        instrument_id=order.instrument_id,
        status=OrderStatus.PENDING
    )
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
