"""Order and trade models for the trading system."""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base, OrderType, OrderSide, OrderStatus

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    instrument_id = Column(Integer, ForeignKey('instruments.id'), nullable=False)
    type = Column(Enum(OrderType), nullable=False)
    side = Column(Enum(OrderSide), nullable=False)
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING)
    quantity = Column(Numeric(20, 8), nullable=False)
    filled_quantity = Column(Numeric(20, 8), default=0)
    price = Column(Numeric(20, 8))  # Limit price or stop price
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    account = relationship('Account', back_populates='orders')
    instrument = relationship('Instrument', back_populates='orders')
    trades = relationship('Trade', back_populates='order')

class Trade(Base):
    __tablename__ = 'trades'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    instrument_id = Column(Integer, ForeignKey('instruments.id'), nullable=False)
    quantity = Column(Numeric(20, 8), nullable=False)
    price = Column(Numeric(20, 8), nullable=False)
    side = Column(Enum(OrderSide), nullable=False)
    executed_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    order = relationship('Order', back_populates='trades')
    account = relationship('Account', back_populates='trades')
    instrument = relationship('Instrument', back_populates='trades')
