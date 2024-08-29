"""Company Model"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from models.user_model import UserResponseModel
from schemas.company_schema import Mode


class CompanyModel(BaseModel):
    """Company Model"""

    id: UUID
    name: str
    description: str
    mode: Mode = Field(default=Mode.UNKNOWN)
    rating: float


class CompanyRequestModel(BaseModel):
    """Model for handling company request parameters.

    Attributes:
        name (Optional[str]): The name of the company.
        description (Optional[str]): A brief description of the company.
        mode (Optional[List[Mode]]): A list of modes associated with the company.
        rating_from (float): The minimum rating filter. Default is 0.0.
        rating_to (float): The maximum rating filter. Default is 5.0.
        page (int): The page number for pagination. Default is 1.
        size (int): The number of items per page for pagination. Default is 15.
    """

    name: Optional[str] = None
    description: Optional[str] = None
    mode: Optional[List[Mode]] = None
    rating_from: float = 0.0
    rating_to: float = 5.0
    page: int = 1
    size: int = 15


class CreateCompanyRequestModel(BaseModel):
    """Model for creating a new company.

    Attributes:
        name (str): The name of the company.
        description (Optional[str]): A brief description of the company.
        mode (Optional[Mode]): The mode associated with the company. Default is Mode.UNKNOWN.
    """

    name: str
    description: Optional[str] = None
    mode: Optional[Mode] = Mode.UNKNOWN


class RateCompanyRequestModel(BaseModel):
    """
    Model for rating a company.

    Attributes:
        id (UUID): The unique identifier of the company.
        rating (float): The rating given to the company.
    """

    id: UUID
    rating: float


class UpdateCompanyRequestModel(BaseModel):
    """
    Model for updating company details.

    Attributes:
        name (Optional[str]): The name of the company.
        description (Optional[str]): A brief description of the company.
        mode (Optional[Mode]): The mode associated with the company.
    """

    name: Optional[str] = None
    description: Optional[str] = None
    mode: Optional[Mode] = None


class CompanyResponseModel(BaseModel):
    """
    Model for company response data.

    Attributes:
        id (UUID): The unique identifier of the company.
        name (str): The name of the company.
        description (str): A brief description of the company.
        mode (Mode): The mode associated with the company.
        rating (float): The rating of the company.
        created_at (datetime): The creation timestamp of the company.
        users (Optional[List[UserResponseModel]]): A list of users associated with the company.
    """

    id: UUID
    name: str
    description: str
    mode: Mode
    rating: float
    created_at: datetime
    users: Optional[List[UserResponseModel]] = None

    class Config:
        """Config"""

        from_attributes = True


class CompanyResponseForAdminModel(CompanyResponseModel):
    """
    Model for company response data with additional admin-specific fields.

    Attributes:
        total_rating_count (int): The total number of ratings the company has received.
        updated_at (datetime): The last update timestamp of the company.
    """

    total_rating_count: int
    updated_at: datetime

    class Config:
        """Config"""
        from_attributes = True
