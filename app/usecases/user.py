from app.models.item import DBItem
from app.models.user import DBUser
from app.repositories.item import ItemRepository
from app.repositories.user import UserRepository
from app.schemas.item import ItemCreate
from app.schemas.user import UserCreate
from app.usecases.errors import DomainException, ErrorDetail


class CreateUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def do(self, user: UserCreate) -> DBUser:
        db_user = self.user_repo.get_by_email(user.email)
        if db_user:
            DomainException(ErrorDetail.ALREADY_EXISTS)

        return self.user_repo.create(user)


class TestTxUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def do(self, user1: UserCreate, user2: UserCreate):
        self.user_repo.create(user1)
        1 / 0  # type: ignore
        self.user_repo.create(user2)


class GetItemsUseCase:
    def __init__(self, item_repo: ItemRepository):
        self.item_repo = item_repo

    def do(self, user_id: int) -> list[DBItem]:
        return self.item_repo.get_by_user_id(user_id)


class CreateItemUseCase:
    def __init__(self, item_repo: ItemRepository):
        self.item_repo = item_repo

    def do(self, item: ItemCreate, user_id: int) -> list[DBItem]:
        return self.item_repo.create_for_user(item, user_id)
