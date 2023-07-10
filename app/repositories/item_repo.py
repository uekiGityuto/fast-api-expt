from sqlalchemy.orm import Session

from app.models.item import DBItem as DBItem
from app.schemas.item import ItemCreate


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DBItem).offset(skip).limit(limit).all()


def get_user_items(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(DBItem).filter(DBItem.owner_id == user_id).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: ItemCreate, user_id: int):
    db_item = DBItem(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
