import enum

from sqlalchemy import Column, Double, Enum, Integer, String, Text
from sqlalchemy.orm import relationship

from config.database import Base
from schemas.base_schema import BaseSchema


class Mode(enum.Enum):
    """
    Enumeration for company modes.

    Attributes:
        HYBRID (str): Represents a hybrid mode.
        ONSITE (str): Represents an onsite mode.
        REMOTE (str): Represents a remote mode.
        UNKNOWN (str): Represents an unknown mode.
    """

    HYBRID = "HYBRID"
    ONSITE = "ONSITE"
    REMOTE = "REMOTER"
    UNKNOWN = "UNKNOWN"


class CompanySchema(BaseSchema, Base):
    """
    Schema for the company table.

    Attributes:
        __tablename__ (str): The name of the database table.
        name (Column): The name of the company. Must be unique and not null.
        description (Column): A brief description of the company.
        mode (Column): The mode of the company. Default is Mode.UNKNOWN.
        rating (Column): The rating of the company. Default is 0.0.
        total_rating_count (Column): 
            The total number of ratings the company has received. 
            Default is 0.
        users (relationship): The relationship to the UserSchema, 
            representing users associated with the company.
    """

    __tablename__ = "companies"

    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    mode = Column(Enum(Mode), default=Mode.UNKNOWN)
    rating = Column(Double, default=0.0)
    total_rating_count = Column(Integer, default=0)
    users = relationship("UserSchema", back_populates="company")
