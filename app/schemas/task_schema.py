"""Task Schema"""

import enum

from sqlalchemy import Column, Enum, ForeignKey, String, Text, Uuid
from sqlalchemy.orm import relationship

from config.database import Base
from schemas.base_schema import BaseSchema


class Status(enum.Enum):
    """
    Enumeration for task statuses.

    Attributes:
        OPEN (str): Task is open.
        TO_DO (str): Task is to be done.
        IN_PROGRESS (str): Task is in progress.
        IN_REVIEW (str): Task is in review.
        APPROVED (str): Task is approved.
        CANCELLED (str): Task is cancelled.
        COMPLETED (str): Task is completed.
        ON_HOLD (str): Task is on hold.
        PENDING_REVIEW (str): Task is pending review.
        DEFERRED (str): Task is deferred.
        BLOCKED (str): Task is blocked.
        READY_FOR_TESTING (str): Task is ready for testing.
        IN_TESTING (str): Task is in testing.
        FAILED_TESTING (str): Task failed testing.
        READY_FOR_DEPLOYMENT (str): Task is ready for deployment.
        DEPLOYED (str): Task is deployed.
        ARCHIVED (str): Task is archived.
        WAITING_FOR_INPUT (str): Task is waiting for input.
    """

    OPEN = "OPEN"
    TO_DO = "TO_DO"
    IN_PROGRESS = "IN_PROGRESS"
    IN_REVIEW = "IN_REVIEW"
    APPROVED = "APPROVED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"
    ON_HOLD = "ON_HOLD"
    PENDING_REVIEW = "PENDING_REVIEW"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"
    READY_FOR_TESTING = "READY_FOR_TESTING"
    IN_TESTING = "IN_TESTING"
    FAILED_TESTING = "FAILED_TESTING"
    READY_FOR_DEPLOYMENT = "READY_FOR_DEPLOYMENT"
    DEPLOYED = "DEPLOYED"
    ARCHIVED = "ARCHIVED"
    WAITING_FOR_INPUT = "WAITING_FOR_INPUT"


class Priority(enum.Enum):
    """
    Enumeration for task priorities.

    Attributes:
        HIGHEST (str): Highest priority.
        HIGH (str): High priority.
        MEDIUM (str): Medium priority.
        LOW (str): Low priority.
        LOWEST (str): Lowest priority.
    """

    HIGHEST = "HIGHEST"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    LOWEST = "LOWEST"


class TaskSchema(BaseSchema, Base):
    """
    Schema for the task table.

    Attributes:
        __tablename__ (str): The name of the database table.
        summary (Column): A brief summary of the task. Cannot be null.
        description (Column): A detailed description of the task. Cannot be null.
        status (Column): The current status of the task. Default is Status.OPEN.
        priority (Column): The priority level of the task. Default is Priority.MEDIUM.
        user_id (Column): The unique identifier of the user associated with the task.
        user (relationship): The relationship to the UserSchema, representing the user associated with the task.
    """

    __tablename__ = "tasks"

    summary = Column(String, nullable=False, default="")
    description = Column(Text, nullable=False, default="")
    status = Column(Enum(Status), default=Status.OPEN, nullable=False)
    priority = Column(Enum(Priority), default=Priority.MEDIUM, nullable=False)
    user_id = Column(Uuid, ForeignKey("users.id"), nullable=True)
    user = relationship("UserSchema", back_populates="tasks")
