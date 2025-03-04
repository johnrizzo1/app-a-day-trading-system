"""Database models for the trading system."""
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.orm import declarative_base, relationship
import enum

Base = declarative_base()

class ModelStatus(enum.Enum):
    DRAFT = "draft"
    TRAINING = "training"
    READY = "ready"
    FAILED = "failed"

class OrderType(enum.Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"

class OrderSide(enum.Enum):
    BUY = "buy"
    SELL = "sell"

class OrderStatus(enum.Enum):
    PENDING = "pending"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"

class Model(Base):
    __tablename__ = "models"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    parameters = Column(JSON)
    status = Column(Enum(ModelStatus), default=ModelStatus.DRAFT)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    strategies = relationship("Strategy", back_populates="model")

class Strategy(Base):
    __tablename__ = "strategies"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    model_id = Column(Integer, ForeignKey("models.id"))
    parameters = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    model = relationship("Model", back_populates="strategies")
    backtests = relationship("Backtest", back_populates="strategy")

class Backtest(Base):
    __tablename__ = "backtests"
    
    id = Column(Integer, primary_key=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id"))
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    initial_capital = Column(Float, nullable=False)
    metrics = Column(JSON)  # Stores Sharpe ratio, returns, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    
    strategy = relationship("Strategy", back_populates="backtests")

class Account(Base):
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    balance = Column(Float, default=0.0)
    margin_enabled = Column(Integer, default=True)
    margin_ratio = Column(Float, default=0.1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    orders = relationship("Order", back_populates="account")

class Instrument(Base):
    __tablename__ = "instruments"
    
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)  # e.g., 'FUTURES', 'SPOT', etc.
    symbol = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    currency = Column(String, nullable=False)
    is_active = Column(Integer, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    orders = relationship("Order", back_populates="instrument")

class FuturesContract(Base):
    __tablename__ = "futures_contracts"
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String, nullable=False)
    expiry = Column(DateTime, nullable=False)
    tick_size = Column(Float, nullable=False)
    contract_size = Column(Float, nullable=False)
    margin_requirement = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Position(Base):
    __tablename__ = "positions"
    
    id = Column(Integer, primary_key=True)
    contract_id = Column(Integer, ForeignKey("futures_contracts.id"))
    quantity = Column(Float, nullable=False)
    entry_price = Column(Float, nullable=False)
    current_price = Column(Float, nullable=False)
    unrealized_pnl = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    instrument_id = Column(Integer, ForeignKey("instruments.id"))
    contract_id = Column(Integer, ForeignKey("futures_contracts.id"))
    type = Column(Enum(OrderType), nullable=False)
    side = Column(Enum(OrderSide), nullable=False)
    quantity = Column(Float, nullable=False)
    filled_quantity = Column(Float)
    price = Column(Float)  # Null for market orders
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    account = relationship("Account", back_populates="orders")
    instrument = relationship("Instrument", back_populates="orders")
    contract = relationship("FuturesContract")
