import uuid
from typing import Optional
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: Optional[str] = Field(None)
    is_superuser: bool = Field(False)


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class User(UserBase):
    id: uuid.UUID
    is_superuser: bool

    class Config:
        from_attributes = True


class UserCreateDB(UserBase):
    hashed_password: Optional[str] = None


class UserUpdateDB(UserBase):
    hashed_password: str
