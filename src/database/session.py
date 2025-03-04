"""Database session management."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os
from typing import Generator

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://trading:trading@postgres:5432/trading_system")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    """Get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
