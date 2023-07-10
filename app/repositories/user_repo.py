from sqlalchemy.orm import Session

from app.core.auth import get_password_hash
from app.models.user import DBUser
from app.schemas.user import UserCreate


def get_user(db: Session, user_id: int):
    return db.query(DBUser).filter(DBUser.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(DBUser).filter(DBUser.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DBUser).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = DBUser(
        email=user.email, hashed_password=hashed_password, admin=user.admin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
