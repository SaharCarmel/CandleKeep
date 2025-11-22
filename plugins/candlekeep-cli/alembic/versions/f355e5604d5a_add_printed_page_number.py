"""add_printed_page_number

Revision ID: f355e5604d5a
Revises: 004b54bd914e
Create Date: 2025-11-22 21:35:02.199073

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f355e5604d5a'
down_revision: Union[str, Sequence[str], None] = '004b54bd914e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add printed_page_number column to book_images table
    op.add_column('book_images', sa.Column('printed_page_number', sa.Integer(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Remove printed_page_number column
    op.drop_column('book_images', 'printed_page_number')
