import enum
from typing import List
import uuid
from config.database import Base
from schemas.base_schema import BaseSchema
from sqlalchemy import Column, Double, Enum, ForeignKey, Integer, String, Text, Uuid, event
from sqlalchemy.orm import relationship

from schemas.base_schema import BaseSchema
from config.database import Base


class Status(enum.Enum):
    OPEN = "OPEN"
    TO_DO = "TO_DO"
    IN_PROGRESS = "IN_PROGRESS"
    IN_REVIEW = "IN_REVIEW"
    APPROVED = "APPROVED"
    DONE = "DONE"
    CANCELLED = "CANCELLED"


class Priority(enum.Enum):
    HIGHEST = "HIGHEST"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    LOWEST = "LOWEST"


class TaskSchema(BaseSchema, Base):
    __tablename__ = "tasks"

    summary = Column(String, nullable=False, default="")
    description = Column(Text, nullable=False, default="")
    status = Column(Enum(Status), default=Status.OPEN, nullable=False)
    priority = Column(Enum(Priority), default=Priority.MEDIUM, nullable=False)
    user_id = Column(Uuid, ForeignKey("users.id"), nullable=True)
    user = relationship("UserSchema", back_populates="tasks")

@event.listens_for(TaskSchema, "before_insert")
def hash_password(mapper, connection, target):
    if not target.status:
        target.status = Status.OPEN
    if not target.priority:
        target.priority = Priority.MEDIUM
