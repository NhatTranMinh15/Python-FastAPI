"""Add Task Table

Revision ID: 582cffdbfba3
Revises: 0b2ae1f593c6
Create Date: 2024-08-23 17:23:08.344346

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '582cffdbfba3'
down_revision: Union[str, None] = '41c31c3065fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
