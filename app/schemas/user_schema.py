from passlib.context import CryptContext
from sqlalchemy import Boolean, Column, ForeignKey, String, Uuid, event
from sqlalchemy.orm import validates

from config.database import Base
from schemas.base_schema import BaseSchema
from sqlalchemy.orm import relationship

bcrypt = CryptContext(schemes=["bcrypt"])


class UserSchema(BaseSchema, Base):
    __tablename__ = "users"

    email = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    is_admin = Column(Boolean, nullable=False, default=False)
    company_id = Column(Uuid, ForeignKey("companies.id"))
    company = relationship("CompanySchema")

    @validates("email")
    def validate_email(self, _, value):
        if "@" not in value:
            raise ValueError("Invalid Email Address")
        return value


# Event listener to hash password before insert
@event.listens_for(UserSchema, "before_insert")
def hash_password(mapper, connection, target):
    target.hashed_password = bcrypt.hash(target.hashed_password)
