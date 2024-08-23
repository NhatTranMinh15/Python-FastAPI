from typing import List
from uuid import UUID

from fastapi_pagination import Page

from config.database import db_dependency
from fastapi import APIRouter, Depends, Query
from models.user_model import (
    CreateUserRequestModel,
    UpdateUserRequestModel,
    UserRequestModel,
    UserResponseForAdminModel,
    UserResponseModel,
)
from services import user_service as UserService
from services.exceptions import ResourceNotFoundException
from sqlalchemy.orm import Session
from starlette import status

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", status_code=status.HTTP_200_OK, response_model=Page[UserResponseModel])
async def get_all_user(
    user_request: UserRequestModel = Depends(),
    junction_type: str = Query(default="OR"),
    db: Session = db_dependency,
):
    print(user_request)
    users = UserService.get_all_users(db, user_request, junction_type)
    return users


@router.get(
    "/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponseModel
)
async def get_one_user(user_id: UUID, db: Session = db_dependency):
    user = UserService.get_one_user_by_id(db, user_id)
    if not user:
        raise ResourceNotFoundException()
    return user


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=UserResponseForAdminModel
)
async def create_user(
    user_request: CreateUserRequestModel, db: Session = db_dependency
):
    # auth check

    #
    return UserService.create_user(db, user_request)


@router.post(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseForAdminModel,
)
async def de_activate_user(
    user_id: UUID, action: str = Query(), db: Session = db_dependency
):
    return UserService.de_activate_user(db, user_id, action)


@router.patch(
    "/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponseModel
)
async def update_user(
    user_id: UUID, user_request: UpdateUserRequestModel, db: Session = db_dependency
):
    return UserService.update_user(db, user_id, user_request)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, db: Session = db_dependency):
    UserService.delete_user(db, user_id)
