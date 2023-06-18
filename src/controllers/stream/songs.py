from utils.db.db import get_session
from controllers.db.models import Songs
from sqlalchemy import select
from fastapi import Depends
from routers.auth import get_current_user


async def fetch_songs_from_db(current_user = Depends(get_current_user)):
    async with get_session() as session:
        stmt = select(Songs)
        result = await session.execute(stmt)
        songs = result.scalars().all()

    return songs