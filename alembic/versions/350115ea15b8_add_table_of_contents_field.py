"""add_table_of_contents_field

Revision ID: 350115ea15b8
Revises: e5ffbf97468e
Create Date: 2025-11-01 17:03:15.297500

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '350115ea15b8'
down_revision: Union[str, Sequence[str], None] = 'e5ffbf97468e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add table_of_contents JSON column
    op.add_column('books', sa.Column('table_of_contents', sa.JSON(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Remove table_of_contents column
    op.drop_column('books', 'table_of_contents')
