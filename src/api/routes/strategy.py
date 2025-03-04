"""Strategy management API endpoints."""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from ..database import get_db
from ...database.models import Strategy, Model

router = APIRouter(prefix="/api/strategies", tags=["strategies"])

class StrategyCreate(BaseModel):
    name: str
    model_id: int
    parameters: dict

class StrategyResponse(BaseModel):
    id: int
    name: str
    model_id: int
    parameters: dict
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

@router.post("/", response_model=StrategyResponse)
async def create_strategy(strategy: StrategyCreate, db: Session = Depends(get_db)):
    # Verify model exists
    model = db.query(Model).filter(Model.id == strategy.model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    db_strategy = Strategy(**strategy.dict())
    db.add(db_strategy)
    try:
        db.commit()
        db.refresh(db_strategy)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return db_strategy

@router.get("/", response_model=List[StrategyResponse])
async def list_strategies(db: Session = Depends(get_db)):
    return db.query(Strategy).all()

@router.get("/{strategy_id}", response_model=StrategyResponse)
async def get_strategy(strategy_id: int, db: Session = Depends(get_db)):
    strategy = db.query(Strategy).filter(Strategy.id == strategy_id).first()
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy

@router.put("/{strategy_id}", response_model=StrategyResponse)
async def update_strategy(
    strategy_id: int, strategy_update: StrategyCreate, db: Session = Depends(get_db)
):
    strategy = db.query(Strategy).filter(Strategy.id == strategy_id).first()
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    
    # Verify model exists if model_id is being updated
    if strategy_update.model_id != strategy.model_id:
        model = db.query(Model).filter(Model.id == strategy_update.model_id).first()
        if not model:
            raise HTTPException(status_code=404, detail="Model not found")
    
    for key, value in strategy_update.dict().items():
        setattr(strategy, key, value)
    
    try:
        db.commit()
        db.refresh(strategy)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return strategy
