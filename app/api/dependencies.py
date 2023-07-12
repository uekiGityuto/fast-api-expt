from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.api.errors import ErrorDetail, raise_http_exception
from app.core.config import settings
from app.db.session import SessionLocal
from app.repositories.user import UserRepository
from app.schemas.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    # TODO: エラーレスポンス周りは改善の余地あり
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=ErrorDetail.INVALID_CREDENTIALS,
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")  # type: ignore
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user_repo = UserRepository(db)
    user = user_repo.get_by_email(email=email)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.active:
        raise_http_exception(status.HTTP_400_BAD_REQUEST,
                             ErrorDetail.INACTIVE_USER)
    return current_user


def get_current_admin_user(current_user: User = Depends(get_current_active_user)) -> User:
    if not current_user.admin:
        raise_http_exception(status.HTTP_403_FORBIDDEN,
                             ErrorDetail.UNAUTHORIZED_OPERATION)
    return current_user
