"""Add Company Table

Revision ID: 0b2ae1f593c6
Revises: 41c31c3065fd
Create Date: 2024-08-23 17:04:48.074981

"""

from datetime import datetime
from typing import Sequence, Union
import uuid

from alembic import op
import sqlalchemy as sa

from schemas.company_schema import Mode


# revision identifiers, used by Alembic.
revision: str = "0b2ae1f593c6"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    companies_table = op.create_table(
        "companies",
        sa.Column("id", sa.UUID, primary_key=True, default=uuid.uuid4),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("mode", sa.Enum(Mode), default=Mode.UNKNOWN),
        sa.Column("rating", sa.Double, default=0.0),
        sa.Column("created_at", sa.Time, nullable=False, default=datetime.now),
        sa.Column(
            "updated_at",
            sa.Time,
            nullable=False,
            default=datetime.now,
            onupdate=datetime.now,
        ),
    )
    op.bulk_insert(
        companies_table,
        [
            {
                "id": uuid.uuid4(),
                "name": "All Company",
                "description": "Description Company",
                "mode": "UNKNOWN",
                "rating": 5,
            },
            {
                "id": uuid.uuid4(),
                "name": "One Company",
                "description": "Description Company one",
                "mode": "REMOTE",
                "rating": 4,
            },
            {
                "id": uuid.uuid4(),
                "name": "Two Company",
                "description": "Description Company Two",
                "mode": "ONSITE",
                "rating": 3,
            },
            {
                "id": uuid.uuid4(),
                "name": "Three Company",
                "description": "Bad",
                "mode": "HYBRID",
                "rating": 1,
            }
        ],
    )


def downgrade() -> None:
    op.drop_table("companies")
    op.execute("DROP TYPE mode;")
