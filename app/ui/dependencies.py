from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.repositories.user import UserRepository
from app.schemas.user import User
from app.ui.errors import handle_error
from app.usecases.errors import AuthException, DomainException, ErrorDetail
from app.usecases.login import GetLoginedUseCase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_current_user(session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)) -> User:
    user_repo = UserRepository(session)
    usecase = GetLoginedUseCase(user_repo)
    try:
        user = usecase.do(token)
    except Exception as e:
        handle_error(e)
        raise  # handle_errorで例外を処理した後にraiseすることで、Pylanceに例外をraiseしたことを知らせる。この処理は実行されない。
    else:
        return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.active:
        handle_error(DomainException(ErrorDetail.INACTIVE_USER))
    return current_user


def get_current_admin_user(current_user: User = Depends(get_current_active_user)) -> User:
    if not current_user.admin:
        handle_error(AuthException(ErrorDetail.UNAUTHORIZED_OPERATION))
    return current_user
