from utils.db.db import get_session
from controllers.db.models import Songs


async def add_song(request):
    async with get_session() as session:
        new_song = Songs(
            artist=request.artist,
            title=request.title
        )

        session.add(new_song)
        await session.commit()
        await session.refresh(new_song)
    return new_song