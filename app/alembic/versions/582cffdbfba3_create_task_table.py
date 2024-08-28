"""Create Task Table

Revision ID: 582cffdbfba3
Revises: 
Create Date: 2024-08-23 17:23:08.344346

"""

from datetime import datetime
import random
from typing import Sequence, Union
import uuid
from alembic import op
import sqlalchemy as sa
from services.name_generator import name
from schemas.task_schema import Priority, Status


# revision identifiers, used by Alembic.
revision: str = "582cffdbfba3"
down_revision: Union[str, None] = "41c31c3065fd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    task_table = op.create_table(
        "tasks",
        sa.Column("id", sa.UUID, primary_key=True, default=uuid.uuid4),
        sa.Column("summary", sa.String, nullable=False, default=""),
        sa.Column("description", sa.Text, nullable=False, default=""),
        sa.Column("status", sa.Enum(Status), default=Status.OPEN, nullable=False),
        sa.Column(
            "priority", sa.Enum(Priority), default=Priority.MEDIUM, nullable=False
        ),
        sa.Column("user_id", sa.UUID),
        sa.Column("created_at", sa.DateTime, nullable=False, default=datetime.now),
        sa.Column(
            "updated_at",
            sa.DateTime,
            nullable=False,
            default=datetime.now,
            onupdate=datetime.now,
        ),
    )

    task_array = []
    for i in range(name.task_length):
        t = {
            "id": uuid.uuid4(),
            "summary": name.task[i],
            "description": name.task_description[i],
            "status": random.choice(list(Status)),
            "priority": random.choice(list(Priority)),
        }
        task_array.append(t)
    op.bulk_insert(task_table, task_array)


def downgrade() -> None:
    op.drop_table("tasks")
    op.execute("DROP TYPE status;")
    op.execute("DROP TYPE priority;")
