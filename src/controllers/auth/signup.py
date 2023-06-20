from utils.db.db import get_session
from controllers.db.models import UserModel
from schemas.auth_schema import User
from .hashing import Hash
import uuid
from sqlalchemy import select, or_
from fastapi import status, HTTPException


async def create_user(request: User):
    async with get_session() as session:
        stmt = select(UserModel).filter(or_(UserModel.username == request.username, UserModel.email == request.email))
        result = await session.execute(stmt)
        existing_user = result.scalars().first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'User already exists')


        new_user = UserModel(
            uuid = str(uuid.uuid4()),
            username = request.username,
            email = request.email,
            password = Hash.bcrypt(request.password)
        )

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
    return new_user