""" Authentication Services

    Raises:
        ForbiddenException
        UnauthorizedException
        UnauthorizedException
        ForbiddenException
        UnauthorizedException
    """

from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from fastapi import Depends
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from config.settings import JWT_ALGORITHM, JWT_SECRET, oa2_bearer
from schemas.user_schema import UserSchema, verify_password
from services import user_service as UserService
from services.exceptions import ForbiddenException, UnauthorizedException


def get_current_utc_time():
    """Get the current time

    Returns:
        datetime: The current time
    """
    return datetime.now(timezone.utc)


def authenticate_user(db: Session, username: str, password: str):
    """Authenticate a user using username and password

    Args:
        db (Session): Database Session
        username (str): username
        password (str): password

    Raises:
        ForbiddenException:
        UnauthorizedException:

    Returns:
        UserSchema: The user
    """
    user = UserService.get_one_user(db, "username", username)
    if not user.is_active:
        raise ForbiddenException("You have been blocked")
    if not verify_password(password, user.hashed_password):
        raise UnauthorizedException()

    return user


def create_access_token(user: UserSchema, expires: Optional[timedelta] = None):
    """Create JWT token

    Args:
        user (UserSchema): User infomation
        expires (Optional[timedelta], optional): Exprire time. Defaults is 30 minutes.

    Returns:
        str: The JWT token
    """
    claims = {
        "sub": user.username,
        "id": str(user.id),
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_admin": user.is_admin,
    }
    expire = (
        get_current_utc_time() + expires
        if expires
        else get_current_utc_time() + timedelta(minutes=60)
    )
    claims.update({"exp": expire})
    return jwt.encode(claims, JWT_SECRET, algorithm=JWT_ALGORITHM)


def token_interceptor(
    token: str = Depends(oa2_bearer), allow_user: bool = False
) -> UserSchema:
    """Extaract JWT token from request header and verify it

    Args:
        token (str, optional): The extracted JWT token
        allow_user (bool, optional): Allow normal user to procced or not. Default is not

    Raises:
        UnauthorizedException:
        ForbiddenException:
        UnauthorizedException:

    Returns:
        UserSchema: The user information inside the JWT token
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user = UserSchema()
        user.username = payload.get("sub")
        user.id = UUID(payload.get("id"))
        user.first_name = payload.get("first_name")
        user.last_name = payload.get("last_name")
        user.is_admin = payload.get("is_admin")

        if user.username is None or user.id is None:
            raise UnauthorizedException()
        if not allow_user and not user.is_admin:
            raise ForbiddenException()
        return user
    except JWTError as exc:
        raise UnauthorizedException() from exc


def get_token_interceptor(allow_user: bool = False):
    """Wrapper function ti get JWT token

    Args:
        allow_user (bool, optional): Allow normal user to proceed or not Defaults to False.
    """

    def dependency(token: str = Depends(oa2_bearer)) -> UserSchema:
        return token_interceptor(token, allow_user)

    return dependency
