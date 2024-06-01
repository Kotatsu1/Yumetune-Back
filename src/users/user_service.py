from fastapi import HTTPException, status
from typing import Optional
import uuid
from .user_schemas import UserCreate, User, UserCreateDB, UserUpdate, UserUpdateDB
from .user_models import UserModel
from .user_dao import UserDAO
from database import async_session_maker
from utils import get_password_hash
from .exceptions import *



class UserService:
    @classmethod
    async def register_new_user(cls, user: UserCreate) -> UserModel:
        async with async_session_maker() as session:
            user_exist = await UserDAO.find_one_or_none(session, email=user.email)
            if user_exist:
                raise UserExistsException

            user.is_superuser = False
            user.is_verified = False
            db_user = await UserDAO.add(
                session,
                UserCreateDB(
                    **user.model_dump(),
                    hashed_password=get_password_hash(user.password))
            )
            await session.commit()

        return db_user

    @classmethod
    async def get_user(cls, user_id: uuid.UUID) -> UserModel:
        async with async_session_maker() as session:
            db_user = await UserDAO.find_one_or_none(session, id=user_id)
        if db_user is None:
            raise UserNotFoundException
        return db_user

    @classmethod
    async def update_user(cls, user_id: uuid.UUID, user: UserUpdate) -> UserModel:
        async with async_session_maker() as session:
            db_user = await UserDAO.find_one_or_none(session, UserModel.id == user_id)
            if db_user is None:
                raise UserNotFoundException

            if user.password:
                user_in = UserUpdateDB(
                    **user.model_dump
                    (
                        exclude={'is_active', 'is_verified', 'is_superuser'},
                        exclude_unset=True
                    ),
                    hashed_password=get_password_hash(user.password)
                )
            else:
                user_in = UserUpdateDB(**user.model_dump())

            user_update = await UserDAO.update(
                session,
                UserModel.id == user_id,
                obj_in=user_in)
            await session.commit()
            return user_update

    @classmethod
    async def delete_user(cls, user_id: uuid.UUID):
        async with async_session_maker() as session:
            db_user = await UserDAO.find_one_or_none(session, id=user_id)
            if db_user is None:
                raise UserNotFoundException

            await UserDAO.update(
                session,
                UserModel.id == user_id,
                {'is_active': False}
            )
            await session.commit()

    @classmethod
    async def get_users_list(cls, *filter, offset: Optional[int] = 0, limit: Optional[int] = 100, **filter_by) -> list[UserModel]:
        async with async_session_maker() as session:
            users = await UserDAO.find_all(session, *filter, offset=offset, limit=limit, **filter_by)
        if users is None:
            raise UserNotFoundException

        return users


    @classmethod
    async def update_user_from_superuser(cls, user_id: uuid.UUID, user: UserUpdate) -> User:
        async with async_session_maker() as session:
            db_user = await UserDAO.find_one_or_none(session, UserModel.id == user_id)
            if db_user is None:
                raise UserNotFoundException

            user_in = UserUpdateDB(**user.model_dump(exclude_unset=True))
            user_update = await UserDAO.update(
                session,
                UserModel.id == user_id,
                obj_in=user_in)
            await session.commit()
            return user_update

    @classmethod
    async def delete_user_from_superuser(cls, user_id: uuid.UUID):
        async with async_session_maker() as session:
            await UserDAO.delete(session, UserModel.id == user_id)
            await session.commit()
