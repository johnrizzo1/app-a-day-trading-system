"""Add updated_at column to futures_contracts table."""
from sqlalchemy import text
from sqlalchemy.orm import Session
from src.database.session import engine

def run_migration():
    """Add updated_at column to futures_contracts table if it doesn't exist."""
    with Session(engine) as session:
        # Check if column exists
        result = session.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='futures_contracts' AND column_name='updated_at'
        """))
        
        if not result.fetchone():
            print("Adding updated_at column to futures_contracts table...")
            session.execute(text("""
                ALTER TABLE futures_contracts 
                ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            """))
            session.commit()
            print("Migration completed successfully.")
        else:
            print("Column already exists, no migration needed.")

if __name__ == "__main__":
    run_migration()
