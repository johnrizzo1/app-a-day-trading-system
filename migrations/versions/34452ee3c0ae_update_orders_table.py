"""Update orders table

Revision ID: 34452ee3c0ae
Revises: 24452ee3c0ae
Create Date: 2025-03-04 13:55:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '34452ee3c0ae'
down_revision: Union[str, None] = '24452ee3c0ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add contract_id column to orders table
    op.add_column('orders', sa.Column('contract_id', sa.Integer(), nullable=True))
    
    # Add foreign key constraint
    op.create_foreign_key(None, 'orders', 'futures_contracts', ['contract_id'], ['id'])
    
    # Make contract_id not nullable after adding it
    op.alter_column('orders', 'contract_id', nullable=False)
    
    # No need to drop or rename tables


def downgrade() -> None:
    # Drop the foreign key constraint
    op.drop_constraint(None, 'orders', type_='foreignkey')
    
    # Drop the contract_id column
    op.drop_column('orders', 'contract_id')
