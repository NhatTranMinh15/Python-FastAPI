"""User Services"""

from uuid import UUID

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session, joinedload

from models.user_model import (
    CreateUserRequestModel,
    UpdateUserRequestModel,
    UserRequestModel,
)
from schemas.user_schema import UserSchema
from services.exceptions import (
    ConflictException,
    ForbiddenException,
    InvalidInputException,
    ResourceNotFoundException,
)


def get_all_users(
    db: Session, user_request: UserRequestModel, junction_type: str
) -> Page[UserSchema]:
    """Get all users

    Args:
        db (Session): Database Session
        user_request (UserRequestModel): Filter parameters
        junction_type (str): Parameters join type. Either "AND" or "OR". Default to "AND"

    Returns:
        Page[UserSchema]: One page of users
    """
    query = select(UserSchema).filter(UserSchema.is_active)

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


def get_one_user(db: Session, var_name, var_value, join: bool = False) -> UserSchema:
    """Get one user infomation

    Args:
        db (Session): Database Session
        var_name (_type_): Filter Attribute
        var_value (_type_): Attribute value
        join (bool, optional): Get user's company. Default to False

    Raises:
        ResourceNotFoundException

    Returns:
        UserSchema: One user infomation
    """
    filter_condition = getattr(UserSchema, var_name) == var_value
    query = select(UserSchema).filter(filter_condition)
    if join:
        query.options(joinedload(UserSchema.company))
    user = db.scalars(query).first()
    if not user:
        raise ResourceNotFoundException()
    return user


def create_user(db: Session, user_request: CreateUserRequestModel) -> UserSchema:
    """Create one user

    Args:
        db (Session): Database Session
        user_request (CreateUserRequestModel): User infomation to be created

    Raises:
        ConflictException: f username or email already existed
    Returns:
        UserSchema: Newly created user
    """
    email = user_request.email
    username = user_request.username
    user = db.scalars(
        select(UserSchema).filter(
            or_(UserSchema.username == username, UserSchema.email == email)
        )
    ).first()
    if user:
        raise ConflictException()

    user_schema = UserSchema(**user_request.model_dump())
    db.add(user_schema)
    db.commit()
    db.refresh(user_schema)

    return user_schema


def update_user(
    db: Session,
    user_id: UUID,
    user_request: UpdateUserRequestModel,
    user_token: UserSchema,
) -> UserSchema:
    """Update user infomation

    Args:
        db (Session): Database Session
        user_id (UUID): user ID to be updated
        user_request (UpdateUserRequestModel): Update Information
        user_token (UserSchema): JWT Token

    Raises:
        ForbiddenException: If normal user try to change other user information

    Returns:
        UserSchema: Updated User
    """
    user: UserSchema = get_one_user(db, "id", user_id)

    if user_token.id != user.id:
        if not user.is_admin:
            raise ForbiddenException(
                "You do not have permission to change this user infomation"
            )
    if user_request.username:
        user.username = user_request.username
    if user_request.first_name:
        user.first_name = user_request.first_name
    if user_request.last_name:
        user.last_name = user_request.last_name

    db.commit()
    db.refresh(user)

    return user


def de_activate_user(db: Session, user_id: UUID, action: str) -> UserSchema:
    """Activate or deactivate user

    Args:
        db (Session): Database Session
        user_id (UUID): User ID
        action (str): Type of action. Either "ACTIVATE" or "DEACTIVATE"

    Raises:
        InvalidInputException: If wrong action

    Returns:
        UserSchema: User information
    """
    user: UserSchema = get_one_user(db, "id", user_id)

    if action.lower() == "activate":
        user.is_active = True
    elif action.lower() == "deactivate":
        user.is_active = False
    else:
        raise InvalidInputException("Wrong Action")
    db.commit()
    db.refresh(user)

    return user


def delete_user(db: Session, user_id: UUID, user_token: UserSchema):
    """Delete one user

    Args:
        db (Session): Database Session
        user_id (UUID): User ID to be deleted
        user_token (UserSchema): JWT token

    Raises:
        ForbiddenException:
    """
    user: UserSchema = get_one_user(db, "id", user_id)

    if user_token.id != user.id:
        if not user.is_admin:
            raise ForbiddenException("You do not have permission to delete this user")
    db.delete(user)
    db.commit()
