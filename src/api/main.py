"""FastAPI application entry point."""
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime
import uvicorn
from sqlalchemy.orm import Session

from src.api.database import get_db
# Direct import from models.py to avoid circular imports
import importlib.util
import os

# Directly import the models.py file
models_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'models.py')
spec = importlib.util.spec_from_file_location('models_module', models_path)
models_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(models_module)

# Get the models from the imported module
Base = models_module.Base
Model = models_module.Model
Strategy = models_module.Strategy
Backtest = models_module.Backtest
FuturesContract = models_module.FuturesContract
Position = models_module.Position
OrderModel = models_module.Order

app = FastAPI(title="Trading System API")

# Pydantic models for request validation
class ModelCreate(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]

class StrategyCreate(BaseModel):
    name: str
    model_id: int
    parameters: Dict[str, Any]

class BacktestCreate(BaseModel):
    strategy_id: int
    start_date: datetime
    end_date: datetime
    initial_capital: float

class FuturesContractCreate(BaseModel):
    symbol: str
    expiry: datetime
    tick_size: float
    contract_size: float
    margin_requirement: float

class OrderCreate(BaseModel):
    contract_id: int
    order_type: str
    side: str
    quantity: float
    price: Optional[float] = None

@app.get("/")
async def root():
    return {"status": "running"}

@app.post("/api/models/")
async def create_model(model: ModelCreate, db: Session = Depends(get_db)):
    """Create a new model."""
    try:
        db_model = Model(
            name=model.name,
            description=model.description,
            parameters=model.parameters
        )
        db.add(db_model)
        db.commit()
        db.refresh(db_model)
        return db_model
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/strategies/")
async def create_strategy(strategy: StrategyCreate, db: Session = Depends(get_db)):
    """Create a new strategy."""
    try:
        db_strategy = Strategy(
            name=strategy.name,
            model_id=strategy.model_id,
            parameters=strategy.parameters
        )
        db.add(db_strategy)
        db.commit()
        db.refresh(db_strategy)
        return db_strategy
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/backtests/")
async def create_backtest(backtest: BacktestCreate, db: Session = Depends(get_db)):
    """Create a new backtest."""
    try:
        db_backtest = Backtest(
            strategy_id=backtest.strategy_id,
            start_date=backtest.start_date,
            end_date=backtest.end_date,
            initial_capital=backtest.initial_capital
        )
        db.add(db_backtest)
        db.commit()
        db.refresh(db_backtest)
        return db_backtest
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/trading/contracts")
async def create_contract(contract: FuturesContractCreate, db: Session = Depends(get_db)):
    """Create a new futures contract."""
    try:
        db_contract = FuturesContract(
            symbol=contract.symbol,
            expiry=contract.expiry,
            tick_size=contract.tick_size,
            contract_size=contract.contract_size,
            margin_requirement=contract.margin_requirement
        )
        db.add(db_contract)
        db.commit()
        db.refresh(db_contract)
        return db_contract
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/trading/orders")
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    """Create a new order."""
    try:
        db_order = OrderModel(
            contract_id=order.contract_id,
            order_type=order.order_type,
            side=order.side,
            quantity=order.quantity,
            price=order.price
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/trading/positions")
async def get_positions(db: Session = Depends(get_db)):
    """Get current positions."""
    try:
        positions = db.query(Position).all()
        return positions
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
