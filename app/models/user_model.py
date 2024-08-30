"""User Model"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserModel(BaseModel):
    """User Model"""

    id: UUID
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    hashed_password: str
    is_active: bool
    is_admin: bool


class UserRequestModel(BaseModel):
    """
    Model for handling user request parameters.

    Attributes:
        email (Optional[str]): The email of the user.
        username (Optional[str]): The username of the user.
        first_name (Optional[str]): The first name of the user.
        last_name (Optional[str]): The last name of the user.
        page (int): The page number for pagination. Default is 1.
        size (int): The number of items per page for pagination. Default is 15.
    """

    email: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    page: int = 1
    size: int = 15


class CreateUserRequestModel(BaseModel):
    """
    Model for creating a new user.

    Attributes:
        email (EmailStr): The email of the user.
        username (str): The username of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        hashed_password (str): The hashed password of the user.
        company_id (Optional[UUID]): The unique identifier of the company associated with the user.
        is_admin (bool): Indicates if the user has admin privileges. Default is False.
    """

    email: EmailStr
    username: str
    first_name: str
    last_name: str
    hashed_password: str
    company_id: Optional[UUID] = None
    is_admin: bool = False


class UpdateUserRequestModel(BaseModel):
    """
    Model for updating user details.

    Attributes:
        username (Optional[str]): The username of the user.
        first_name (Optional[str]): The first name of the user.
        last_name (Optional[str]): The last name of the user.
    """

    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserResponseModel(BaseModel):
    """
    Model for user response data.

    Attributes:
        id (UUID): The unique identifier of the user.
        email (str): The email of the user.
        username (str): The username of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        created_at (datetime): The creation timestamp of the user.
        is_admin (bool): Indicates if the user has admin privileges.
        company_id (Optional[UUID]): The unique identifier of the company associated with the user.
    """

    id: UUID
    email: str
    username: str
    first_name: str
    last_name: str
    created_at: datetime
    is_admin: bool
    company_id: Optional[UUID] = None

    class Config:
        """Config"""

        from_attributes = True


class UserResponseForAdminModel(UserResponseModel):
    """
    Model for user response data with additional admin-specific fields.

    Attributes:
        is_active (bool): Indicates if the user account is active.
        is_admin (bool): Indicates if the user has admin privileges.
    """

    is_active: bool
    is_admin: bool

    class Config:
        """Config"""

        from_attributes = True

class Token():
    """JWT Token Model"""
    id: UUID
    email: str
    username: str
    first_name: str
    last_name: str
    is_admin: bool