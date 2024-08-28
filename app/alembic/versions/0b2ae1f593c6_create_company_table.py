"""Create Company Table

Revision ID: 0b2ae1f593c6
Revises: 
Create Date: 2024-08-23 17:04:48.074981

"""

import random
import uuid
from datetime import datetime
from typing import Sequence, Union

import sqlalchemy as sa
from schemas.company_schema import Mode
from services.name_generator import name, name_gen

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0b2ae1f593c6"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    companies_table = op.create_table(
        "companies",
        sa.Column("id", sa.UUID, primary_key=True, default=uuid.uuid4),
        sa.Column("name", sa.String, unique=True, nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("mode", sa.Enum(Mode), default=Mode.UNKNOWN),
        sa.Column("rating", sa.Double, default=0.0),
        sa.Column("total_rating_count", sa.Integer, default=0),
        sa.Column("created_at", sa.DateTime, nullable=False, default=datetime.now),
        sa.Column(
            "updated_at",
            sa.DateTime,
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
                "total_rating_count": 10,
            },
            {
                "id": uuid.uuid4(),
                "name": "One Company",
                "description": "Description Company one",
                "mode": "REMOTE",
                "rating": 4,
                "total_rating_count": 10,
            },
            {
                "id": uuid.uuid4(),
                "name": "Two Company",
                "description": "Description Company Two",
                "mode": "ONSITE",
                "rating": 3,
                "total_rating_count": 10,
            },
            {
                "id": uuid.uuid4(),
                "name": "Three Company",
                "description": "Bad",
                "mode": "HYBRID",
                "rating": 1,
                "total_rating_count": 10,
            },
        ],
    )
    company_array = []
    for i in range(name.company_length):
        c = {
            "id": uuid.uuid4(),
            "name": name.company[i],
            "description": name.company_description[i],
            "mode": random.choice(list(Mode)),
            "rating": round(random.uniform(0, 5), 2),
            "total_rating_count": random.randrange(1, 100),
        }
        company_array.append(c)
    op.bulk_insert(companies_table, company_array)


def downgrade() -> None:
    op.drop_table("companies")
    op.execute("DROP TYPE mode;")
