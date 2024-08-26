"""Add User table

Revision ID: 41c31c3065fd
Revises: 
Create Date: 2024-08-23 16:53:39.186979

"""

from datetime import datetime
from typing import Sequence, Union
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "41c31c3065fd"
down_revision: Union[str, None] = "0b2ae1f593c6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    users_table = op.create_table(
        "users",
        sa.Column("id", sa.UUID, primary_key=True, default=uuid.uuid4),
        sa.Column("email", sa.String, unique=True, nullable=False),
        sa.Column("username", sa.String, nullable=False),
        sa.Column("first_name", sa.String),
        sa.Column("last_name", sa.String),
        sa.Column("hashed_password", sa.String, nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, default=True),
        sa.Column("is_admin", sa.Boolean, nullable=False, default=False),
        sa.Column("company_id", sa.UUID),
        sa.Column("created_at", sa.DateTime, nullable=False, default=datetime.now),
        sa.Column(
            "updated_at",
            sa.DateTime,
            nullable=False,
            default=datetime.now,
            onupdate=datetime.now,
        ),
    )
    op.create_foreign_key(
        "fk_user_company", "users", "companies", ["company_id"], ["id"]
    )
    op.bulk_insert(
        users_table,
        [
            {
                "email": "admin@mail.com",
                "username": "admin",
                "first_name": "First",
                "last_name": "Admin",
                "hashed_password": "$2b$12$a2m15MlDX9IqkUfUmd1f6./6XdnnVIKGJslXA9oRe8XqkeC9SgBAW", # admin
                "is_admin": True,
            }
        ],
    )


def downgrade() -> None:
    op.drop_column("users", "company_id")
    op.drop_table("users")
