"""Create User table

Revision ID: 41c31c3065fd
Revises: 
Create Date: 2024-08-23 16:53:39.186979

"""

import uuid
from datetime import datetime
from random import random, randrange
from typing import Sequence, Union

import sqlalchemy as sa
from passlib.context import CryptContext
from services.name_generator import name_gen

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "41c31c3065fd"
down_revision: Union[str, None] = "0b2ae1f593c6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


bcrypt = CryptContext(schemes=["bcrypt"])


def gen_user():
    first_name = name_gen.get_first_name()
    last_name = name_gen.get_last_name()
    username = name_gen.get_username(first_name + " " + last_name)
    email = name_gen.get_email(first_name + " " + last_name)
    return [first_name, last_name, username, email]


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
                "hashed_password": "$2b$12$a2m15MlDX9IqkUfUmd1f6./6XdnnVIKGJslXA9oRe8XqkeC9SgBAW",  # admin
                "is_admin": True,
            }
        ],
    )
    data = []
    password = bcrypt.hash("password")
    for i in range(100):
        [first_name, last_name, username, email] = gen_user()
        user = {
            "email": email + str(randrange(100)) + "@mail.com",
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "hashed_password": password,  # email
            "is_admin": False if random() < 0.9 else True,
        }
        print(f"Adding user {i+1} of 100")
        data.append(user)
    op.bulk_insert(users_table, data)


def downgrade() -> None:
    op.drop_column("users", "company_id")
    op.drop_table("users")
