import enum
from typing import List
import uuid
from config.database import Base
from schemas.base_schema import BaseSchema
from sqlalchemy import Column, Double, Enum, Integer, String, Text, Uuid
from sqlalchemy.orm import relationship


class Mode(enum.Enum):
    HYBRID = "HYBRID"
    ONSITE = "ONSITE"
    REMOTE = "REMOTER"
    UNKNOWN = "UNKNOWN"


class CompanySchema(BaseSchema, Base):
    __tablename__ = "companies"

    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    mode = Column(Enum(Mode), default=Mode.UNKNOWN)
    rating = Column(Double, default=0.0)
    total_rating_count = Column(Integer, default=0)
    users = relationship("UserSchema", back_populates="company")
