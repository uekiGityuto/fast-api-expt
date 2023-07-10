from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_active_user, get_db
from app.api.errors import ErrorDetail, raise_http_exception
from app.repositories import user_repo
from app.repositories import item_repo
from app.schemas.item import Item, ItemCreate
from app.schemas.user import User, UserCreate

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("", response_model=User)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.post("", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_repo.get_user_by_email(db, email=user.email)
    if db_user:
        raise_http_exception(status.HTTP_400_BAD_REQUEST,
                             ErrorDetail.USER_ALREADY_EXISTS)
    return user_repo.create_user(db=db, user=user)


@router.get("/items", response_model=list[Item])
def read_own_items(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return item_repo.get_user_items(db=db, user_id=current_user.id)


@router.post("/items", response_model=Item)
def create_items(item: ItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return item_repo.create_user_item(db=db, item=item, user_id=current_user.id)
