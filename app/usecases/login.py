from datetime import datetime, timedelta

from jose import JWTError, jwt

from app.core.config import settings
from app.core.hash import verify_password
from app.models.user import DBUser
from app.repositories.user import UserRepository
from app.schemas.user import User
from app.usecases.errors import AuthException, ErrorDetail


class LoginUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def _create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    def _authenticate_user(self, email: str, password: str) -> DBUser:
        user = self.user_repo.get_by_email(email)
        if user is None:
            raise AuthException(ErrorDetail.LOGIN_FAILED)
        assert user is not None
        if not verify_password(password, user.hashed_password):
            raise AuthException(ErrorDetail.LOGIN_FAILED)
        return user

    def do(self, username: str, password: str) -> str:
        user = self._authenticate_user(username, password)
        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return self._create_access_token({"sub": user.email}, access_token_expires)


class GetLoginedUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def do(self, token: str) -> User:
        e = AuthException(ErrorDetail.INVALID_CREDENTIALS)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY,
                                 algorithms=[settings.ALGORITHM])
            email = payload.get("sub")
            if email is None:
                raise e
        except JWTError:
            raise e
        user = self.user_repo.get_by_email(email=email)
        if user is None:
            raise e
        return user
