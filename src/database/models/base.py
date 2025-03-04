"""Base models for the trading system."""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Numeric, Boolean
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from enum import Enum as PyEnum
from typing import Optional

Base = declarative_base()

class InstrumentType(str, PyEnum):
    EQUITY = 'equity'
    BOND = 'bond'
    FUTURES = 'futures'
    
class OrderType(str, PyEnum):
    MARKET = 'market'
    LIMIT = 'limit'
    STOP = 'stop'
    STOP_LIMIT = 'stop_limit'
    
class OrderSide(str, PyEnum):
    BUY = 'buy'
    SELL = 'sell'
    
class OrderStatus(str, PyEnum):
    PENDING = 'pending'
    FILLED = 'filled'
    PARTIALLY_FILLED = 'partially_filled'
    CANCELLED = 'cancelled'
    REJECTED = 'rejected'
    
class TradingSession(str, PyEnum):
    PRE_MARKET = 'pre_market'
    REGULAR = 'regular'
    AFTER_HOURS = 'after_hours'

class Instrument(Base):
    __tablename__ = 'instruments'
    
    id = Column(Integer, primary_key=True)
    type = Column(Enum(InstrumentType), nullable=False)
    symbol = Column(String, unique=True, nullable=False)
    name = Column(String)
    description = Column(String)
    currency = Column(String, default='USD')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Price information
    last_price = Column(Numeric(20, 8))
    daily_high = Column(Numeric(20, 8))
    daily_low = Column(Numeric(20, 8))
    daily_volume = Column(Numeric(20, 8))
    timestamp = Column(DateTime)
    
    # Relationships
    orders = relationship('Order', back_populates='instrument')
    positions = relationship('Position', back_populates='instrument')
    trades = relationship('Trade', back_populates='instrument')
    
    __mapper_args__ = {
        'polymorphic_identity': 'instrument',
        'polymorphic_on': type
    }
