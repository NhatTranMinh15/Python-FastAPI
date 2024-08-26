from typing import List
from uuid import UUID

from fastapi_pagination import Page, Params

from models.user_model import (
    CreateUserRequestModel,
    UpdateUserRequestModel,
    UserRequestModel,
)
from schemas.user_schema import UserSchema
from services.exceptions import (
    BadRequestException,
    ConflictException,
    InvalidInputException,
    ResourceNotFoundException,
)
from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate


def get_all_users(
    db: Session, user_request: UserRequestModel, junction_type: str
) -> Page[UserSchema]:
    query = select(UserSchema).filter(UserSchema.is_active == True)

    if user_request is not None:
        conditions = []
        if user_request.username:
            conditions.append(UserSchema.username.like(f"%{user_request.username}%"))
        if user_request.email:
            conditions.append(UserSchema.email == user_request.email)
        if user_request.first_name:
            conditions.append(UserSchema.first_name.like(f"{user_request.first_name}%"))
        if user_request.last_name:
            conditions.append(UserSchema.last_name.like(f"{user_request.last_name}%"))

        if junction_type == "OR":
            query = query.filter(or_(*conditions))
        elif junction_type == "AND":
            query = query.filter(and_(*conditions))

    return paginate(
        db, query, params=Params(size=user_request.size, page=user_request.page)
    )


def get_one_user_by_id(db: Session, user_id: UUID) -> UserSchema:
    user = db.scalars(select(UserSchema).filter(UserSchema.id == user_id)).first()
    if not user:
        raise ResourceNotFoundException()
    return user

def get_one_user_by_email(db: Session, user_email: str) -> UserSchema:
    return db.scalars(select(UserSchema).filter(UserSchema.email == user_email)).first()


def create_user(db: Session, user_request: CreateUserRequestModel):
    email = user_request.email
    user: UserSchema = get_one_user_by_email(db, email)
    if user:
        raise ConflictException()
    
    user_schema = UserSchema(**user_request.model_dump())
    db.add(user_schema)
    db.commit()
    db.refresh(user_schema)

    return user_schema


def update_user(db: Session, user_id: UUID, user_request: UpdateUserRequestModel):
    user: UserSchema = get_one_user_by_id(db, user_id)
    if not user:
        raise ResourceNotFoundException()

    if user_request.username:
        user.username = user_request.username
    if user_request.first_name:
        user.first_name = user_request.first_name
    if user_request.last_name:
        user.last_name = user_request.last_name

    db.commit()
    db.refresh(user)

    return user


def de_activate_user(db: Session, user_id: UUID, action: str):
    user: UserSchema = get_one_user_by_id(db, user_id)

    if not user:
        raise ResourceNotFoundException()

    if action == "activate":
        user.is_active = True
    elif action == "deactivate":
        user.is_active = False
    else:
        raise InvalidInputException("Wrong Action")
    db.commit()
    db.refresh(user)

    return user


def delete_user(db: Session, user_id: UUID):
    user: UserSchema = get_one_user_by_id(db, user_id)

    if not user:
        raise ResourceNotFoundException()

    db.delete(user)
    db.commit()
