from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi.params import Query
from fastapi_pagination import Params
from pydantic import BaseModel, EmailStr, Field

from models.user_model import UserResponseModel
from schemas.company_schema import Mode


class CompanyModel(BaseModel):
    id: UUID
    name: str
    description: str
    mode: Mode = Field(default=Mode.UNKNOWN)
    rating: float


class CompanyRequestModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    mode: Optional[List[Mode]] = None
    rating_from: float = 0.0
    rating_to: float = 5.0
    page: int = 1
    size: int = 15


class CreateCompanyRequestModel(BaseModel):
    name: str
    description: Optional[str] = None
    mode: Optional[Mode] = Mode.UNKNOWN


class RateCompanyRequestModel(BaseModel):
    id: UUID
    rating: float


class UpdateCompanyRequestModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    mode: Optional[Mode] = None


class CompanyResponseModel(BaseModel):
    id: UUID
    name: str
    description: str
    mode: Mode
    rating: float
    created_at: datetime
    users: Optional[List[UserResponseModel]] = None

    class Config:
        from_attributes = True


class CompanyResponseForAdminModel(CompanyResponseModel):
    total_rating_count: int
    updated_at: datetime

    class Config:
        from_attributes = True
