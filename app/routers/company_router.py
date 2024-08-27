from typing import List, Optional
from uuid import UUID

from fastapi_pagination import Page
from sqlalchemy import select

from models.company_model import (
    CompanyRequestModel,
    CompanyResponseModel,
    CreateCompanyRequestModel,
    RateCompanyRequestModel,
    UpdateCompanyRequestModel,
)
from schemas.company_schema import CompanySchema, Mode
from config.database import db_dependency
from fastapi import APIRouter, Body, Depends, Query
from services.exceptions import ResourceNotFoundException
from sqlalchemy.orm import Session
from starlette import status
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
):
    return CompanyService.get_all_companies(db, company_request, mode, junction_type)


@router.get(
    "/{company_id}", status_code=status.HTTP_200_OK, response_model=CompanyResponseModel
)
async def get_one_company(company_id: UUID, db: Session = db_dependency):
    return CompanyService.get_one_company(db, company_id)


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=CompanyResponseModel
)
async def create_company(
    company_request: CreateCompanyRequestModel, db: Session = db_dependency
):
    company = CompanyService.create_company(db, company_request)
    return company


@router.post(
    "/rate", status_code=status.HTTP_200_OK, response_model=CompanyResponseModel
)
async def rate_company(
    rate_request: RateCompanyRequestModel, db: Session = db_dependency
):
    company = CompanyService.rate_company(db, rate_request)
    return company


@router.post(
    "/user", status_code=status.HTTP_200_OK, response_model=CompanyResponseModel
)
async def add_or_remove_user(
    company_id: UUID = Body(),
    user_id: UUID = Body(),
    action: str = Body(),
    db: Session = db_dependency,
):
    company = CompanyService.add_or_remove_user(db, company_id, user_id, action)    
    return company


@router.patch(
    "/{company_id}", status_code=status.HTTP_200_OK, response_model=CompanyResponseModel
)
async def update_company(
    company_id: UUID,
    company_request: UpdateCompanyRequestModel,
    db: Session = db_dependency,
):
    company = CompanyService.update_company(db, company_id, company_request)
    return company


@router.delete("/{company_id}", status_code=status.HTTP_200_OK)
async def delete_company(company_id: UUID, db: Session = db_dependency):
    return db.scalars(select(CompanySchema)).all()
