from controllers.db.models import Songs, Playlists, PlaylistContent
from utils.db.db import get_session
from datetime import datetime
from schemas.playlist_schema import CreatePlaylist, ManagePlaylist
from sqlalchemy import select, delete
from fastapi import HTTPException, status, Depends
from routers.auth import get_current_user


async def create_playlist(request: CreatePlaylist, current_user = Depends(get_current_user)):
    async with get_session() as session:
        new_playlist = Playlists(
            name = request.name,
            user_uuid = current_user
        )
        session.add(new_playlist)
        await session.commit()
        await session.refresh(new_playlist)
    return {'msg': 'Playlist created successfully'}


# async def get_playlist_content(current_user = Depends(get_current_user)):
#     async with get_session() as session:
#         stmt = select(PlaylistContent).filter(PlaylistContent.song_id == request.song_id, PlaylistContent.playlist_id == request.playlist_id)
#         result = await session.execute(stmt)
#         existing_library_item = result.scalars().first()
#         if existing_library_item:
#             raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'Library item already exists')
        

async def add_song(request: ManagePlaylist, current_user = Depends(get_current_user)):
    async with get_session() as session:

        stmt = select(PlaylistContent).filter(PlaylistContent.song_id == request.song_id, PlaylistContent.playlist_id == request.playlist_id)
        result = await session.execute(stmt)
        existing_playlist_item = result.scalars().first()
        if existing_playlist_item:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'Playlist item already exists')

        new_playlist_item = PlaylistContent(
            song_id = request.song_id,
            playlist_id = request.playlist_id,
            added_at = datetime.now(),

        )

        session.add(new_playlist_item)
        await session.commit()
        await session.refresh(new_playlist_item)
    return {'msg': 'Song added successfully'}

# async def remove_song(request: Library, current_user = Depends(get_current_user)):
#     async with get_session() as session:
#         stmt = delete(UserLibrary).filter(UserLibrary.song_id == request.song_id, UserLibrary.user_uuid == current_user)
#         await session.execute(stmt)
#         await session.commit()
#     return {'msg': 'Song removed successfully'}