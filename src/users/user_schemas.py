import uuid
from typing import Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: Optional[str] = Field(None)
    is_active: bool = Field(True)
    is_verified: bool = Field(False)
    is_superuser: bool = Field(False)


class UserCreate(UserBase):
    username: str
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class User(UserBase):
    id: uuid.UUID
    username: str
    is_active: bool
    is_verified: bool
    is_superuser: bool

    class Config:
        from_attributes = True


class UserCreateDB(UserBase):
    hashed_password: Optional[str] = None


class UserUpdateDB(UserBase):
    hashed_password: str
