from typing import List
from uuid import UUID

from fastapi import HTTPException
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from schemas.user_schema import UserSchema
from models.company_model import (
    CompanyRequestModel,
    CreateCompanyRequestModel,
    RateCompanyRequestModel,
    UpdateCompanyRequestModel,
)
from schemas.company_schema import CompanySchema, Mode
from services.exceptions import BadRequestException, ResourceNotFoundException
from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session, joinedload
from services import user_service as UserService


def get_all_companies(
    db: Session,
    company_request: CompanyRequestModel,
    mode: List[Mode],
    junction_type: str,
) -> Page[CompanySchema]:
    query = select(CompanySchema)
    conditions = []
    if company_request.name:
        conditions.append(CompanySchema.name.like(f"{company_request.name}%"))
    if company_request.description:
        conditions.append(
            CompanySchema.description.like(f"%{company_request.description}%")
        )
    if mode:
        conditions.append(CompanySchema.mode.in_(mode))
    conditions.append(
        CompanySchema.rating.between(
            company_request.rating_from, company_request.rating_to
        )
    )
    if junction_type == "OR":
        query = query.filter(or_(*conditions))
    elif junction_type == "AND":
        query = query.filter(and_(*conditions))
    page = paginate(
        db, query, params=Params(size=company_request.size, page=company_request.page)
    )
    return page


def get_one_company(db: Session, company_id: UUID):
    company = db.scalars(
        select(CompanySchema)
        .options(joinedload(CompanySchema.users))
        .filter(CompanySchema.id == company_id)
    ).first()
    if not company:
        raise ResourceNotFoundException()
    return company


def create_company(db: Session, company_request: CreateCompanyRequestModel):
    company_schema = CompanySchema(**company_request.model_dump())
    db.add(company_schema)
    db.commit()
    db.refresh(company_schema)
    return company_schema


def rate_company(db: Session, rate_company_request: RateCompanyRequestModel):
    company_id = rate_company_request.id
    company = get_one_company(db, company_id)
    rating = rate_company_request.rating
    total_count = company.total_rating_count
    old_rating = company.rating
    new_rating: float = ((old_rating * total_count) + rating) * 1.0 / (total_count + 1)
    company.rating = new_rating
    company.total_rating_count = total_count + 1
    db.commit()
    db.refresh(company)
    return company


def update_company(
    db: Session, company_id: UUID, company_request: UpdateCompanyRequestModel
):
    company = get_one_company(db, company_id)
    if company_request.name:
        company.name = company_request.name
    if company_request.description:
        company.description = company_request.description
    if company_request.mode:
        company.mode = company_request.mode

    db.commit()
    db.refresh(company)
    return company


def add_or_remove_user(db: Session, company_id: UUID, user_id: UUID, action: str):
    company = get_one_company(db, company_id)
    user = UserService.get_one_user_by_id(db, user_id)
    if action == "ADD":
        company.users.append(user)
    elif action == "REMOVE":
        try:
            company.users.remove(user)
        except:
            raise BadRequestException(f"User {user.username} is not in this company")
    else:
        raise BadRequestException(f"There is no {action} action")

    db.commit()
    db.refresh(company)

    return company
