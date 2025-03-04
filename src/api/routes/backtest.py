"""Backtesting API endpoints."""
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from ..database import get_db
from ...database.models import Backtest, Strategy
from ...services.backtest import run_backtest

router = APIRouter(prefix="/api/backtests", tags=["backtests"])

class BacktestCreate(BaseModel):
    strategy_id: int
    start_date: datetime
    end_date: datetime
    initial_capital: float

class BacktestResponse(BaseModel):
    id: int
    strategy_id: int
    start_date: datetime
    end_date: datetime
    initial_capital: float
    metrics: Optional[dict]
    created_at: datetime

    class Config:
        orm_mode = True

@router.post("/", response_model=BacktestResponse)
async def create_backtest(
    backtest: BacktestCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Verify strategy exists
    strategy = db.query(Strategy).filter(Strategy.id == backtest.strategy_id).first()
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    
    # Validate dates
    if backtest.end_date <= backtest.start_date:
        raise HTTPException(status_code=400, detail="End date must be after start date")
    
    db_backtest = Backtest(**backtest.dict())
    db.add(db_backtest)
    try:
        db.commit()
        db.refresh(db_backtest)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
    # Run backtest in background
    background_tasks.add_task(run_backtest, db_backtest.id)
    return db_backtest

@router.get("/", response_model=List[BacktestResponse])
async def list_backtests(
    strategy_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Backtest)
    if strategy_id:
        query = query.filter(Backtest.strategy_id == strategy_id)
    return query.all()

@router.get("/{backtest_id}", response_model=BacktestResponse)
async def get_backtest(backtest_id: int, db: Session = Depends(get_db)):
    backtest = db.query(Backtest).filter(Backtest.id == backtest_id).first()
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return backtest
