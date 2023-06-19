from controllers.db.models import UserLibrary, Songs
from utils.db.db import get_session
from datetime import datetime
from schemas.library_schema import Library
from sqlalchemy import select
from fastapi import HTTPException, status


async def get_user_library():
    async with get_session() as session:
        ...


async def add_song(request: Library):
    async with get_session() as session:
        stmt = select(UserLibrary).filter(UserLibrary.song_id == request.song_id, UserLibrary.user_uuid == request.user_uuid)
        result = await session.execute(stmt)
        existing_library_item = result.scalars().first()
        if existing_library_item:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'Library item already exists')

        new_library_item = UserLibrary(
            song_id = request.song_id,
            play_count = 0,
            added_at = datetime.now(),
            user_uuid = request.user_uuid
        )

        session.add(new_library_item)
        await session.commit()
        await session.refresh(new_library_item)
    return new_library_item

async def remove_song():
    return 