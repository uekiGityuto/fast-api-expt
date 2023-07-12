from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_admin_user, get_db
from app.api.errors import ErrorDetail, raise_http_exception
from app.repositories.item import ItemRepo
from app.repositories.user import UserRepo
from app.schemas.item import Item, ItemCreate
from app.schemas.user import User

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_current_admin_user)],
)


@router.get("/users", response_model=list[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user_repo = UserRepo(db)
    users = user_repo.get_all(skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user_repo = UserRepo(db)
    db_user = user_repo.get_by_id(user_id=user_id)
    if db_user is None:
        raise_http_exception(status.HTTP_404_NOT_FOUND,
                             ErrorDetail.USER_NOT_FOUND)
    return db_user


@router.delete("/users/{user_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_repo = UserRepo(db)
    is_deleted = user_repo.delete_by_id(user_id=user_id)
    if not is_deleted:
        raise_http_exception(status.HTTP_404_NOT_FOUND,
                             ErrorDetail.USER_NOT_FOUND)
    return status.HTTP_204_NO_CONTENT


@router.post("/users/{user_id}/items", response_model=Item)
def create_item_for_user(user_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    item_repo = ItemRepo(db)
    return item_repo.create_for_user(item=item, user_id=user_id)


@router.get("/items", response_model=list[Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    item_repo = ItemRepo(db)
    items = item_repo.get_all(skip=skip, limit=limit)
    return items
