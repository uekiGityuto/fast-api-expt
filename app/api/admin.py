from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_admin_user, get_db
from app.api.errors import ErrorDetail, raise_http_exception
from app.repositories import item_repo, user_repo
from app.schemas.item import Item, ItemCreate
from app.schemas.user import User

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_current_admin_user)],
)


@router.get("/users", response_model=list[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_repo.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_repo.get_user(db, user_id=user_id)
    if db_user is None:
        raise_http_exception(status.HTTP_404_NOT_FOUND,
                             ErrorDetail.USER_NOT_FOUND)
    return db_user


@router.delete("/users/{user_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    is_deleted = user_repo.delete_user(db, user_id=user_id)
    if not is_deleted:
        raise_http_exception(status.HTTP_404_NOT_FOUND,
                             ErrorDetail.USER_NOT_FOUND)
    return status.HTTP_204_NO_CONTENT


@router.post("/users/{user_id}/items", response_model=Item)
def create_item_for_user(user_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    return item_repo.create_user_item(db=db, item=item, user_id=user_id)


@router.get("/items", response_model=list[Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = item_repo.get_items(db, skip=skip, limit=limit)
    return items
