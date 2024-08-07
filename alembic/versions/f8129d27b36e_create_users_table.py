"""create users table

Revision ID: f8129d27b36e
Revises: 8a76db945d04
Create Date: 2024-08-07 11:54:35.294035

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f8129d27b36e'
down_revision: Union[str, None] = '8a76db945d04'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
