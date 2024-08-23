from datetime import datetime
import uuid

from sqlalchemy import Column, Time, Uuid, event


class BaseSchema:
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    created_at = Column(Time, nullable=False, default=datetime.now)
    updated_at = Column(
        Time, nullable=False, default=datetime.now, onupdate=datetime.now
    )


# Event listeners to set created_at and updated_at
@event.listens_for(BaseSchema, "before_insert")
def set_created_at(mapper, connection, target):
    target.created_at = datetime.now()
    target.updated_at = datetime.now()


@event.listens_for(BaseSchema, "before_update")
def set_updated_at(mapper, connection, target):
    target.updated_at = datetime.now()
