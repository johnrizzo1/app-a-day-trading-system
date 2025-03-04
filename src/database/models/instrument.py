"""Instrument models for the trading system."""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from .base import Base, InstrumentType

class Equity(Base):
    __tablename__ = 'equities'
    
    id = Column(Integer, ForeignKey('instruments.id'), primary_key=True)
    sector = Column(String)
    industry = Column(String)
    market_cap = Column(Numeric(20, 2))
    pe_ratio = Column(Float)
    dividend_yield = Column(Float)
    beta = Column(Float)
    
    __mapper_args__ = {
        'polymorphic_identity': InstrumentType.EQUITY
    }

class Bond(Base):
    __tablename__ = 'bonds'
    
    id = Column(Integer, ForeignKey('instruments.id'), primary_key=True)
    issuer = Column(String)
    maturity_date = Column(DateTime)
    coupon_rate = Column(Float)
    face_value = Column(Numeric(20, 2))
    yield_to_maturity = Column(Float)
    credit_rating = Column(String)
    duration = Column(Float)
    
    __mapper_args__ = {
        'polymorphic_identity': InstrumentType.BOND
    }

class FuturesContract(Base):
    __tablename__ = 'futures'
    
    id = Column(Integer, ForeignKey('instruments.id'), primary_key=True)
    underlying = Column(String)
    expiry_date = Column(DateTime)
    contract_size = Column(Integer)
    tick_size = Column(Float)
    initial_margin = Column(Numeric(20, 2))
    maintenance_margin = Column(Numeric(20, 2))
    funding_rate = Column(Float)
    
    __mapper_args__ = {
        'polymorphic_identity': InstrumentType.FUTURES
    }
