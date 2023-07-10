from pydantic import BaseModel
from app.schemas.item import Item


class UserBase(BaseModel):
    email: str
    admin: bool = False


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True
