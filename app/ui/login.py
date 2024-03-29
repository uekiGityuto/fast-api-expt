from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.ui.dependencies import get_session
from app.ui.errors import handle_error
from app.repositories.user import UserRepository
from app.schemas.token import Token
from app.usecases.login import LoginUseCase

router = APIRouter(
    prefix="/login",
    tags=["login"],
)


@router.post("", response_model=Token)
def login_for_access_token(req: Request, form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user_repo = UserRepository(session)
    usecase = LoginUseCase(user_repo)
    try:
        access_token = usecase.do(
            username=form_data.username, password=form_data.password)
    except Exception as e:
        handle_error(e, req)
    else:
        return {"access_token": access_token, "token_type": "bearer"}
