from pydantic import BaseModel, EmailStr
from app.schemas.item import Item


class UserBase(BaseModel):
    email: EmailStr
    admin: bool = False


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True
