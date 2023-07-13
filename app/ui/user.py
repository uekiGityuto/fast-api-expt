from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.repositories.item import ItemRepository
from app.repositories.user import UserRepository
from app.schemas.item import Item, ItemCreate
from app.schemas.user import User, UserCreate
from app.ui.dependencies import get_current_active_user, get_session
from app.ui.errors import handle_error
from app.usecases.user import (CreateItemUseCase, CreateUserUseCase,
                               GetItemsUseCase, TestTxUseCase)

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("", response_model=User)
def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.post("", response_model=User)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    user_repo = UserRepository(session)
    usecase = CreateUserUseCase(user_repo)
    try:
        created = usecase.do(user)
    except Exception as e:
        handle_error(e)
    else:
        return created


@router.post("/tx-test", response_model=None, status_code=status.HTTP_201_CREATED)
def test(session: Session = Depends(get_session)):
    user_repo = UserRepository(session)
    usecase = TestTxUseCase(user_repo)
    user1 = UserCreate(email="test1@example.com",  # type: ignore
                       password="password")
    user2 = UserCreate(email="test2@example.com",  # type: ignore
                       password="password")
    try:
        created = usecase.do(user1, user2)
    except Exception as e:
        handle_error(e)
    else:
        return created


@router.get("/items", response_model=list[Item])
def get_own_items(db: Session = Depends(get_session), current_user: User = Depends(get_current_active_user)):
    item_repo = ItemRepository(db)
    usecase = GetItemsUseCase(item_repo)
    try:
        items = usecase.do(current_user.id)
    except Exception as e:
        handle_error(e)
    else:
        return items


@router.post("/items", response_model=Item)
def create_own_item(item: ItemCreate, db: Session = Depends(get_session), current_user: User = Depends(get_current_active_user)):
    item_repo = ItemRepository(db)
    usecase = CreateItemUseCase(item_repo)
    try:
        created = usecase.do(item, current_user.id)
    except Exception as e:
        handle_error(e)
    else:
        return created
