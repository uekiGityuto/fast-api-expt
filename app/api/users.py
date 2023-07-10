from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api.dependencies import get_current_active_user, get_db
from app.api.errors import ErrorDetail, raise_http_exception

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user


@router.post("", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise_http_exception(status.HTTP_400_BAD_REQUEST,
                             ErrorDetail.USER_ALREADY_EXISTS)
    return crud.create_user(db=db, user=user)


@router.get("/items", response_model=list[schemas.Item])
def read_own_items(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    return crud.get_user_items(db=db, user_id=current_user.id)


@router.post("/items", response_model=schemas.Item)
def create_items(item: schemas.ItemCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    return crud.create_user_item(db=db, item=item, user_id=current_user.id)
