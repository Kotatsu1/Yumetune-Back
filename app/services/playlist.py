from database.models import Songs, Playlist, PlaylistContent
from database.postgresql import get_session
from datetime import datetime
from schemas.playlist_schema import CreatePlaylist
from sqlalchemy import select, delete
from fastapi import HTTPException, status



async def create_playlist(name: str, uuid: str):
    async with get_session() as session:
        new_playlist = Playlist(
            name = name,
            user_uuid = uuid
        )
        session.add(new_playlist)
        await session.commit()
        await session.refresh(new_playlist)
    return {'msg': 'Playlist created successfully'}


async def get_playlist_content(id: int):
    async with get_session() as session:
        stmt = select(PlaylistContent.playlist_content_id, Songs.artist, Songs.title, Songs.length)\
            .join(Songs, PlaylistContent.song_id == Songs.id)\
            .filter(PlaylistContent.fk_playlist_id == id)
        result = await session.execute(stmt)
        playlist_content = result.mappings().all()
    return playlist_content


async def add_song(song_id: int, playlist_id: int):
    async with get_session() as session:

        stmt = select(PlaylistContent).filter(PlaylistContent.song_id == song_id, PlaylistContent.fk_playlist_id == playlist_id)
        result = await session.execute(stmt)
        existing_library_item = result.scalars().first()
        if existing_library_item:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'Playlist item already exists')

        new_playlist_item = PlaylistContent(
            song_id = song_id,
            fk_playlist_id = playlist_id
        )

        session.add(new_playlist_item)
        await session.commit()
        await session.refresh(new_playlist_item)
    return {'msg': 'Song added successfully'}


async def remove_song(song_id, playlist_id):
    async with get_session() as session:
        stmt = delete(PlaylistContent).filter(PlaylistContent.song_id == song_id, PlaylistContent.fk_playlist_id == playlist_id)
        await session.execute(stmt)
        await session.commit()
    return {'msg': 'Song removed successfully'}