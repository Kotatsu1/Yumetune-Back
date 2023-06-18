from utils.db.db import get_session
from controllers.db.models import Songs

from sqlalchemy import select


async def fetch_songs_from_db():
    async with get_session() as session:
        stmt = select(Songs)
        result = await session.execute(stmt)
        songs = result.scalars().all()

    return songs