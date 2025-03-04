"""Configuration management for the trading system."""
from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://trading:trading@localhost:5432/trading_system"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = False
    
    # Market Data
    MARKET_DATA_REFRESH_RATE: float = 1.0
    
    # Trading
    DEFAULT_LEVERAGE: float = 1.0
    MAX_LEVERAGE: float = 10.0
    MARGIN_REQUIREMENT: float = 0.1
    
    # Security
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # External APIs
    ALPHA_VANTAGE_API_KEY: Optional[str] = None
    YAHOO_FINANCE_API_KEY: Optional[str] = None
    BLOOMBERG_API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
