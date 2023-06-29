from database.models import UserLibrary, Songs
from database.postgresql import get_session
from datetime import datetime
from schemas.library_schema import Library
from sqlalchemy import select, delete
from fastapi import HTTPException, status



async def get_user_library(uuid: str):
    async with get_session() as session:

        stmt = select(UserLibrary.library_id, UserLibrary.added_at, UserLibrary.play_count, Songs.artist, Songs.title, Songs.length)\
            .join(Songs, UserLibrary.song_id == Songs.id)\
            .filter(UserLibrary.user_uuid == uuid)
        
        result = await session.execute(stmt)
        library_items = result.mappings().all()
        
        return library_items

async def add_song(request: Library, uuid: str):
    async with get_session() as session:

        stmt = select(UserLibrary).filter(UserLibrary.song_id == request.song_id, UserLibrary.user_uuid == uuid)
        result = await session.execute(stmt)
        existing_library_item = result.scalars().first()
        if existing_library_item:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'Library item already exists')

        new_library_item = UserLibrary(
            song_id = request.song_id,
            play_count = 0,
            added_at = datetime.now(),
            user_uuid = uuid
        )

        session.add(new_library_item)
        await session.commit()
        await session.refresh(new_library_item)
    return {'msg': 'Song added successfully'}

async def remove_song(request: Library, uuid: str):
    async with get_session() as session:
        stmt = delete(UserLibrary).filter(UserLibrary.song_id == request.song_id, UserLibrary.user_uuid == uuid)
        await session.execute(stmt)
        await session.commit()
    return {'msg': 'Song removed successfully'}