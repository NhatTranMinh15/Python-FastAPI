from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi.params import Query
from fastapi_pagination import Params
from pydantic import BaseModel, EmailStr, Field


class UserModel(BaseModel):
    id: UUID
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    hashed_password: str
    is_active: bool
    is_admin: bool


class UserRequestModel(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    page: int = 1
    size: int = 15


class CreateUserRequestModel(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    hashed_password: str
    is_admin: bool= False


class UpdateUserRequestModel(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserResponseModel(BaseModel):
    id: UUID
    email: str
    username: str
    first_name: str
    last_name: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserResponseForAdminModel(UserResponseModel):
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True
