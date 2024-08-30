"""Authentication Route"""

from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from config.database import db_dependency
from services import auth_service as AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = db_dependency,
):
    """
    Handles user login and returns an access token.

    This endpoint authenticates the user using the provided form data (username and password).
    If authentication is successful, it generates and returns an access token.

    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing the username and password.
        db (Session): The database session dependency.

    Returns:
        dict: A dictionary containing the access token and token type.
    """
    user = AuthService.authenticate_user(db, form_data.username, form_data.password)
    return {
        "access_token": AuthService.create_access_token(user, timedelta(minutes=60)),
        "token_type": "bearer",
    }
