from datetime import timedelta

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api.dependencies import get_db
from app.api.errors import ErrorDetail, raise_http_exception
from app.core.auth import create_access_token, verify_password
from app.core.config import settings

router = APIRouter(
    prefix="/login",
    tags=["login"],
)


def authenticate_user(db: Session, email: str, password: str) -> models.User:
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise_http_exception(status.HTTP_403_FORBIDDEN,
                             ErrorDetail.LOGIN_FAILURE)
    assert user is not None
    if not verify_password(password, user.hashed_password):
        raise_http_exception(status.HTTP_403_FORBIDDEN,
                             ErrorDetail.LOGIN_FAILURE)
    return user


@router.post("", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
