"""Account and position models for the trading system."""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Numeric, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Account(Base):
    __tablename__ = 'accounts'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    balance = Column(Numeric(20, 2), default=0)
    margin_enabled = Column(Boolean, default=False)
    margin_ratio = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    positions = relationship('Position', back_populates='account')
    orders = relationship('Order', back_populates='account')
    trades = relationship('Trade', back_populates='account')

class Position(Base):
    __tablename__ = 'positions'
    
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    instrument_id = Column(Integer, ForeignKey('instruments.id'), nullable=False)
    quantity = Column(Numeric(20, 8), nullable=False)
    average_entry_price = Column(Numeric(20, 8), nullable=False)
    unrealized_pnl = Column(Numeric(20, 2))
    realized_pnl = Column(Numeric(20, 2))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    account = relationship('Account', back_populates='positions')
    instrument = relationship('Instrument', back_populates='positions')
