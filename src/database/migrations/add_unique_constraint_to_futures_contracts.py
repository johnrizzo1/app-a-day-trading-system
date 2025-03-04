"""Add unique constraint to symbol column in futures_contracts table."""
from sqlalchemy import text
from sqlalchemy.orm import Session
from src.database.session import engine

def run_migration():
    """Add unique constraint to symbol column in futures_contracts table."""
    with Session(engine) as session:
        # Check if the constraint already exists
        result = session.execute(text("""
            SELECT constraint_name
            FROM information_schema.table_constraints
            WHERE table_name = 'futures_contracts' 
            AND constraint_type = 'UNIQUE'
            AND constraint_name LIKE '%symbol%'
        """))
        
        if not result.fetchone():
            print("Adding unique constraint to symbol column in futures_contracts table...")
            
            # First check if there are any duplicate symbols
            result = session.execute(text("""
                SELECT symbol, COUNT(*) 
                FROM futures_contracts 
                GROUP BY symbol 
                HAVING COUNT(*) > 1
            """))
            
            duplicates = result.fetchall()
            if duplicates:
                print(f"Found duplicate symbols: {duplicates}")
                print("Instead of deleting duplicates (which would violate foreign key constraints),")
                print("we'll rename them to make them unique...")
                
                for symbol, count in duplicates:
                    # Get all the duplicate contracts
                    contracts = session.execute(
                        text("SELECT id FROM futures_contracts WHERE symbol = :symbol ORDER BY created_at"),
                        {"symbol": symbol}
                    ).fetchall()
                    
                    # Skip the first one (keep it as is)
                    for i, (contract_id,) in enumerate(contracts[1:], 1):
                        # Rename the others with a suffix
                        new_symbol = f"{symbol}-{i}"
                        session.execute(
                            text("UPDATE futures_contracts SET symbol = :new_symbol WHERE id = :id"),
                            {"new_symbol": new_symbol, "id": contract_id}
                        )
                        print(f"Renamed contract id {contract_id} from {symbol} to {new_symbol}")
            
            # Now add the unique constraint
            session.execute(text("""
                ALTER TABLE futures_contracts
                ADD CONSTRAINT futures_contracts_symbol_key UNIQUE (symbol)
            """))
            
            session.commit()
            print("Migration completed successfully.")
        else:
            print("Unique constraint already exists, no migration needed.")

if __name__ == "__main__":
    run_migration()
