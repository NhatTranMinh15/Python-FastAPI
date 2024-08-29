"""Company Route"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Query
from fastapi_pagination import Page
from sqlalchemy.orm import Session
from starlette import status

from config.database import db_dependency
from models.company_model import (CompanyRequestModel, CompanyResponseModel,
                                  CreateCompanyRequestModel,
                                  RateCompanyRequestModel,
                                  UpdateCompanyRequestModel)
from schemas.company_schema import Mode
from schemas.user_schema import UserSchema
from services import auth_service as AuthService
from services import company_service as CompanyService

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.get(
    "", status_code=status.HTTP_200_OK, response_model=Page[CompanyResponseModel]
)
async def get_all_companies(
    db: Session = db_dependency,
    mode: Optional[List[Mode]] = Query(None),
    company_request: CompanyRequestModel = Depends(),
    junction_type: str = Query(default="AND"),
    user_token: UserSchema = Depends(
        AuthService.get_token_interceptor(allow_user=True)
    ),
):
    """
    Retrieves a paginated list of companies based on the provided filters.

    Args:
        db (Session): The database session dependency.
        mode (Optional[List[Mode]]): A list of modes to filter companies.
        company_request (CompanyRequestModel): The request model containing company filters.
        junction_type (str): The type of junction for combining filters. Default is "AND".
        user_token (UserSchema): The user token for authentication.

    Returns:
        Page[CompanyResponseModel]: A paginated list of companies.
    """
    return CompanyService.get_all_companies(db, company_request, mode, junction_type)


@router.get(
    "/{company_id}", status_code=status.HTTP_200_OK, response_model=CompanyResponseModel
)
async def get_one_company(
    company_id: UUID,
    db: Session = db_dependency,
    user_token: UserSchema = Depends(
        AuthService.get_token_interceptor(allow_user=True)
    ),
):
    """
    Retrieves details of a specific company by its ID.

    Args:
        company_id (UUID): The unique identifier of the company.
        db (Session): The database session dependency.
        user_token (UserSchema): The user token for authentication.

    Returns:
        CompanyResponseModel: The details of the company.
    """
    return CompanyService.get_one_company(db, company_id)


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=CompanyResponseModel
)
async def create_company(
    company_request: CreateCompanyRequestModel,
    db: Session = db_dependency,
    user_token: UserSchema = Depends(AuthService.get_token_interceptor()),
):
    """
    Creates a new company.

    Args:
        company_request (CreateCompanyRequestModel): The request model containing company details.
        db (Session): The database session dependency.
        user_token (UserSchema): The user token for authentication.

    Returns:
        CompanyResponseModel: The details of the created company.
    """
    company = CompanyService.create_company(db, company_request)
    return company


@router.post(
    "/rate", status_code=status.HTTP_200_OK, response_model=CompanyResponseModel
)
async def rate_company(
    rate_request: RateCompanyRequestModel,
    db: Session = db_dependency,
    user_token: UserSchema = Depends(
        AuthService.get_token_interceptor(allow_user=True)
    ),
):
    """
    Rates a company.

    Args:
        rate_request (RateCompanyRequestModel): The request model containing rating details.
        db (Session): The database session dependency.
        user_token (UserSchema): The user token for authentication.

    Returns:
        CompanyResponseModel: The details of the rated company.
    """
    company = CompanyService.rate_company(db, rate_request)
    return company


@router.post(
    "/user",
    status_code=status.HTTP_200_OK,
    response_model=CompanyResponseModel,
)
async def add_or_remove_user(
    company_id: UUID = Body(),
    user_id: UUID = Body(),
    action: str = Body(),
    db: Session = db_dependency,
    user_token: UserSchema = Depends(AuthService.get_token_interceptor()),
):
    """
    Adds or removes a user from a company.

    Args:
        company_id (UUID): The unique identifier of the company.
        user_id (UUID): The unique identifier of the user.
        action (str): The action to perform ("add" or "remove").
        db (Session): The database session dependency.
        user_token (UserSchema): The user token for authentication.

    Returns:
        CompanyResponseModel: The details of the company after the action.
    """
    company = CompanyService.add_or_remove_user(db, company_id, user_id, action)
    return company


@router.patch(
    "/{company_id}", status_code=status.HTTP_200_OK, response_model=CompanyResponseModel
)
async def update_company(
    company_id: UUID,
    company_request: UpdateCompanyRequestModel,
    db: Session = db_dependency,
    user_token: UserSchema = Depends(AuthService.get_token_interceptor()),
):
    """
    Updates details of a specific company.

    Args:
        company_id (UUID): The unique identifier of the company.
        company_request (UpdateCompanyRequestModel): The request model containing updated company details.
        db (Session): The database session dependency.
        user_token (UserSchema): The user token for authentication.

    Returns:
        CompanyResponseModel: The updated details of the company.
    """
    company = CompanyService.update_company(db, company_id, company_request)
    return company


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    company_id: UUID,
    db: Session = db_dependency,
    user_token: UserSchema = Depends(AuthService.get_token_interceptor()),
):
    """
    Deletes a specific company by its ID.

    Args:
        company_id (UUID): The unique identifier of the company.
        db (Session): The database session dependency.
        user_token (UserSchema): The user token for authentication.

    Returns:
        None
    """
    return CompanyService.delete_company(db, company_id)
