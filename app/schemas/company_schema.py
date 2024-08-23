import enum

from config.database import Base
from schemas.base_schema import BaseSchema
from sqlalchemy import Column, Double, Enum, String, Text
from sqlalchemy.orm import relationship

class Mode(enum.Enum):
    HYBRID = "H"
    ONSITE = "O"
    REMOTE = "R"
    UNKNOWN = "U"


class CompanySchema(BaseSchema, Base):
    __tablename__ = "companies"

    name = Column(String, nullable=False)
    description = Column(Text)
    mode = Column(Enum(Mode), default=Mode.UNKNOWN)
    rating = Column(Double, default=0.0)
    users = relationship("UserSchema", back_populates="company")
