"""Database connection utilities for the API."""
from sqlalchemy.orm import Session
from src.database.session import SessionLocal

def get_db():
    """Dependency for getting a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
