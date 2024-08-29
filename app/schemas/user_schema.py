"""User Schema"""
from sqlalchemy import Boolean, Column, ForeignKey, String, Uuid, event
from sqlalchemy.orm import relationship, validates

from config.database import Base
from config.settings import bcrypt_context
from schemas.base_schema import BaseSchema


class UserSchema(BaseSchema, Base):
    """
    Schema for the user table.

    Attributes:
        __tablename__ (str): The name of the database table.
        email (Column): The email of the user. Must be unique and not null.
        username (Column): The username of the user. Must be unique and not null.
        first_name (Column): The first name of the user.
        last_name (Column): The last name of the user.
        hashed_password (Column): The hashed password of the user. Cannot be null.
        is_active (Column): Indicates if the user account is active. Default is True.
        is_admin (Column): Indicates if the user has admin privileges. Default is False.
        company_id (Column): The unique identifier of the company associated with the user.
        company (relationship): The relationship to the CompanySchema, representing the company associated with the user.
        tasks (relationship): The relationship to the TaskSchema, representing tasks associated with the user.
    """

    __tablename__ = "users"

    email = Column(String, unique=True, nullable=False, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    is_admin = Column(Boolean, nullable=False, default=False)
    company_id = Column(Uuid, ForeignKey("companies.id"), nullable=True)
    company = relationship("CompanySchema", back_populates="users")

    tasks = relationship("TaskSchema", back_populates="user")

    @validates("email")
    def validate_email(self, _, value):
        """
        Validates the email address.

        Args:
            _ (Any): The field being validated.
            value (str): The email address to validate.

        Returns:
            str: The validated email address.

        Raises:
            ValueError: If the email address is invalid.
        """
        if "@" not in value:
            raise ValueError("Invalid Email Address")
        return value


# Event listener to hash password before insert
@event.listens_for(UserSchema, "before_insert")
def hash_password(mapper, connection, target):
    """
    Event listener to hash the password before inserting a new user record.

    Args:
        mapper (Mapper): The mapper.
        connection (Connection): The database connection.
        target (UserSchema): The target user instance.
    """
    target.hashed_password = bcrypt_context.hash(target.hashed_password)


def verify_password(plain_password, hased_password):
    """
    Verifies a plain password against a hashed password.

    Args:
        plain_password (str): The plain password.
        hashed_password (str): The hashed password.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return bcrypt_context.verify(plain_password, hased_password)
