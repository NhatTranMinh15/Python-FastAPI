""" User Route

"""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from fastapi_pagination import Page
from sqlalchemy.orm import Session
from starlette import status

from config.database import db_dependency
from models.user_model import (CreateUserRequestModel, UpdateUserRequestModel,
                               UserRequestModel, UserResponseForAdminModel,
                               UserResponseModel)
from schemas.user_schema import UserSchema
from services import auth_service as AuthService
from services import user_service as UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", status_code=status.HTTP_200_OK, response_model=Page[UserResponseModel])
async def get_all_user(
    user_request: UserRequestModel = Depends(),
    junction_type: str = Query(default="AND"),
    db: Session = db_dependency,
    user_token: UserSchema = Depends(
        AuthService.get_token_interceptor(allow_user=True)
    ),
):
    """Endpoint to retrive infomation of all users. Any user can do this action

    Args:
        user_request (UserRequestModel, optional): Filter parameter. Optional
        junction_type (str, optional): Filter type. Either "AND" or "OR". Defaults "AND".
        db (Session, optional): Database Session. Defaults to db_dependency.
        user_token (UserSchema, optional): JWT token for authentication and authorization. Allow any user who has logged in

    Returns:
        Page[UserResponseModel]: One page of user infomation
    """
    users = UserService.get_all_users(db, user_request, junction_type)
    return users


@router.get(
    "/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponseModel
)
async def get_one_user(
    user_id: UUID,
    db: Session = db_dependency,
    user_token: UserSchema = Depends(
        AuthService.get_token_interceptor(allow_user=True)
    ),
):
    """Endpoint to retrive infomation of one user by their ID. Any user can do this action

    Args:
        user_id (UUID): The ID of the needed user
        db (Session, optional): Database Session. Defaults to db_dependency.
        user_token (UserSchema, optional): JWT token for authentication and authorization. Allow any user who has logged in

    Returns:
        UserResponseModel: User infomation
    """
    user = UserService.get_one_user(db, "id", user_id)
    return user


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=UserResponseForAdminModel
)
async def create_user(
    user_request: CreateUserRequestModel,
    db: Session = db_dependency,
    user_token: UserSchema = Depends(AuthService.get_token_interceptor()),
):
    """Endpoint to create new user. Only admin can do this action

    Args:
        user_request (CreateUserRequestModel): Infomation to create new user
        db (Session, optional): Database Session. Defaults to db_dependency.
        user_token (UserSchema, optional): JWT token for authentication and authorization. Allow admin only

    Returns:
        UserResponseForAdminModel: The newly created user
    """
    return UserService.create_user(db, user_request)


@router.post(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseForAdminModel,
)
async def de_activate_user(
    user_id: UUID,
    action: str = Query(),
    db: Session = db_dependency,
    user_token: UserSchema = Depends(AuthService.get_token_interceptor()),
):
    """Endpoint to activate or deactivate a user using their ID. Only admin can do this action

    Args:
        user_id (UUID): The user ID to be activate or deactivate
        action (str, optional): The action to be perform. Either "ACTIVATE" or "DEACTIVATE"
        db (Session, optional): Database Session. Defaults to db_dependency.
        user_token (UserSchema, optional): JWT token for authentication and authorization. Allow admin only
    Returns:
        UserResponseForAdminModel: The user which was acted on
    """
    return UserService.de_activate_user(db, user_id, action)


@router.patch(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseForAdminModel,
)
async def update_user(
    user_id: UUID,
    user_request: UpdateUserRequestModel,
    db: Session = db_dependency,
    user_token: UserSchema = Depends(
        AuthService.get_token_interceptor(allow_user=True)
    ),
):
    """Endpoint to update a user using their ID.
    Any user can update their account. But only admin can update others

    Args:
        user_id (UUID): The user ID to be updated
        user_request (UpdateUserRequestModel): Request Body. Contain user infomation to be updated
        user_id (UUID): The user ID to be deleted
        db (Session, optional): Database Session. Defaults to db_dependency.
        user_token (UserSchema, optional): JWT token for authentication and authorization. Allow any user who has logged in

    Returns:
        UserResponseForAdminModel: This updated user
    """
    return UserService.update_user(db, user_id, user_request, user_token)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    db: Session = db_dependency,
    user_token: UserSchema = Depends(
        AuthService.get_token_interceptor(allow_user=True)
    ),
):
    """Endpoint to delete a user using their ID.
    Any user can delete their account. But only admin can delete others
    Args:
        user_id (UUID): The user ID to be deleted
        db (Session, optional): Database Session. Defaults to db_dependency.
        user_token (UserSchema, optional): JWT token for authentication and authorization. Allow any user who has logged in
    """
    UserService.delete_user(db, user_id, user_token)
