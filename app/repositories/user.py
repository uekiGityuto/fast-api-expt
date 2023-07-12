from sqlalchemy.orm import Session

from app.core.hash import get_password_hash
from app.models.user import DBUser
from app.schemas.user import UserCreate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> DBUser | None:
        return self.db.query(DBUser).get(user_id)

    def get_by_email(self, email: str) -> DBUser | None:
        return self.db.query(DBUser).filter(DBUser.email == email).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[DBUser]:
        return self.db.query(DBUser).offset(skip).limit(limit).all()

    def create(self, user: UserCreate) -> DBUser:
        hashed_password = get_password_hash(user.password)
        db_user = DBUser(
            email=user.email, hashed_password=hashed_password, admin=user.admin)
        self.db.add(db_user)
        self.db.flush()
        return db_user

    def delete_by_id(self, user_id: int) -> bool:
        user = self.db.query(DBUser).get(user_id)
        if user is None:
            return False
        else:
            self.db.delete(user)
            self.db.flush()
            return True
