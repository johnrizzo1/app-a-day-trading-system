"""Model management API endpoints."""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from ..database import get_db
from ...database.models import FinancialModel, ModelStatus

router = APIRouter(prefix="/api/models", tags=["models"])

class ModelCreate(BaseModel):
    name: str
    description: str
    parameters: dict

class ModelResponse(BaseModel):
    id: int
    name: str
    description: str
    parameters: dict
    status: ModelStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

@router.post("/", response_model=ModelResponse)
async def create_model(model: ModelCreate, db: Session = Depends(get_db)):
    db_model = FinancialModel(**model.dict())
    db.add(db_model)
    try:
        db.commit()
        db.refresh(db_model)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return db_model

@router.get("/", response_model=List[ModelResponse])
async def list_models(db: Session = Depends(get_db)):
    return db.query(FinancialModel).all()

@router.get("/{model_id}", response_model=ModelResponse)
async def get_model(model_id: int, db: Session = Depends(get_db)):
    model = db.query(FinancialModel).filter(FinancialModel.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return model

@router.put("/{model_id}", response_model=ModelResponse)
async def update_model(model_id: int, model_update: ModelCreate, db: Session = Depends(get_db)):
    model = db.query(FinancialModel).filter(FinancialModel.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    for key, value in model_update.dict().items():
        setattr(model, key, value)
    
    try:
        db.commit()
        db.refresh(model)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return model
