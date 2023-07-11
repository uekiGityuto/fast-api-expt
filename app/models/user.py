from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class DBUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    admin = Column(Boolean, default=False, nullable=False)

    items = relationship("DBItem", back_populates="owner",
                         cascade="all, delete-orphan")
