from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.ui.dependencies import get_current_admin_user, get_session
from app.ui.errors import handle_error
from app.repositories.item import ItemRepository
from app.repositories.user import UserRepository
from app.schemas.item import Item, ItemCreate
from app.schemas.user import User
from app.usecases.admin import (DeleteUserUseCase, GetItemsUseCase,
                                GetUsersUseCase, GetUserUseCase)
from app.usecases.user import CreateItemUseCase

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_current_admin_user)],
)


@router.get("/users", response_model=list[User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    user_repo = UserRepository(db)
    usecase = GetUsersUseCase(user_repo)
    try:
        items = usecase.do(skip=skip, limit=limit)
    except Exception as e:
        handle_error(e)
    else:
        return items


@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_session)):
    user_repo = UserRepository(db)
    usecase = GetUserUseCase(user_repo)
    try:
        user = usecase.do(user_id)
    except Exception as e:
        handle_error(e)
    else:
        return user


@router.delete("/users/{user_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_session)):
    user_repo = UserRepository(db)
    usecase = DeleteUserUseCase(user_repo)
    try:
        usecase.do(user_id)
    except Exception as e:
        handle_error(e)
    else:
        return status.HTTP_204_NO_CONTENT


@router.post("/users/{user_id}/items", response_model=Item)
def create_item_for_user(user_id: int, item: ItemCreate, db: Session = Depends(get_session)):
    item_repo = ItemRepository(db)
    usecase = CreateItemUseCase(item_repo)
    try:
        created = usecase.do(item, user_id)
    except Exception as e:
        handle_error(e)
    else:
        return created


@router.get("/items", response_model=list[Item])
def get_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    item_repo = ItemRepository(db)
    usecase = GetItemsUseCase(item_repo)
    try:
        items = usecase.do(skip=skip, limit=limit)
    except Exception as e:
        handle_error(e)
    else:
        return items
