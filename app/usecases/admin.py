from app.models.item import DBItem
from app.models.user import DBUser
from app.repositories.item import ItemRepository
from app.repositories.user import UserRepository
from app.usecases.errors import DomainException, ErrorDetail


class GetUsersUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def do(self, skip: int, limit: int) -> list[DBUser]:
        return self.user_repo.get_all(skip=skip, limit=limit)


class GetUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def do(self, user_id: int) -> DBUser:
        user = self.user_repo.get_by_id(user_id)
        if user is None:
            raise DomainException(ErrorDetail.NOT_FOUND)
        return user


class DeleteUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def do(self, user_id: int):
        if not self.user_repo.delete_by_id(user_id):
            raise DomainException(ErrorDetail.NOT_FOUND)


class GetItemsUseCase:
    def __init__(self, item_repo: ItemRepository):
        self.item_repo = item_repo

    def do(self, skip: int, limit: int) -> list[DBItem]:
        return self.item_repo.get_all(skip=skip, limit=limit)
