from sqlalchemy.orm import Session

from app.models.item import DBItem as DBItem
from app.schemas.item import ItemCreate


class ItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[DBItem]:
        return self.db.query(DBItem).offset(skip).limit(limit).all()

    def get_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100) -> list[DBItem]:
        return self.db.query(DBItem).filter(DBItem.owner_id == user_id).offset(skip).limit(limit).all()

    def create_for_user(self, item: ItemCreate, user_id: int) -> DBItem:
        db_item = DBItem(**item.dict(), owner_id=user_id)
        self.db.add(db_item)
        self.db.flush()
        return db_item
