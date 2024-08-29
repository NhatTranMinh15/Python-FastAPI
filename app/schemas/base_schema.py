"""Base Schema"""

import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Uuid


class BaseSchema:
    """
    Base schema model with common attributes.

    Attributes:
        id (Column): The unique identifier of the record. Default is a new UUID.
        created_at (Column): The timestamp when the record was created. Default is the current datetime.
        updated_at (Column): The timestamp when the record was last updated. Default is the current datetime, updated on each change.
    """

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )
