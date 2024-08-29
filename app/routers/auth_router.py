from datetime import timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from config.database import db_dependency

from services import auth_service as AuthService


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = db_dependency,
):
    user = AuthService.authenticate_user(db, form_data.username, form_data.password)
    return {
        "access_token": AuthService.create_access_token(user, timedelta(minutes=10)),
        "token_type": "bearer",
    }
