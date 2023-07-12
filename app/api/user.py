from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_active_user, get_db
from app.api.errors import ErrorDetail, raise_http_exception
from app.repositories.item import ItemRepository
from app.repositories.user import UserRepository
from app.schemas.item import Item, ItemCreate
from app.schemas.user import User, UserCreate

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("", response_model=User)
def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.post("", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    db_user = user_repo.get_by_email(email=user.email)
    if db_user:
        raise_http_exception(status.HTTP_400_BAD_REQUEST,
                             ErrorDetail.USER_ALREADY_EXISTS)
    return user_repo.create(user=user)


@router.get("/items", response_model=list[Item])
def get_own_items(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    item_repo = ItemRepository(db)
    return item_repo.get_by_user_id(user_id=current_user.id)


@router.post("/items", response_model=Item)
def create_own_item(item: ItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    item_repo = ItemRepository(db)
    return item_repo.create_for_user(item=item, user_id=current_user.id)
