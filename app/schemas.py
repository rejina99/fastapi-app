from pydantic import BaseModel

from database import Base


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: str


class UserCreateLogin(UserLogin):
    password: str


class Login(UserLogin):
    id: int
    is_active: bool

    class ConfigLogin:
        orm_mode = True
