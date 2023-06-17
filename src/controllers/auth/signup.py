from utils.db.db import get_session
from controllers.db.models import UserModel
from schemas.auth_schema import User
from .hashing import Hash
import uuid


async def create_user(request: User):
    async with get_session() as session:
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