from fastapi import APIRouter, Depends
from services import playlist
from schemas.playlist_schema import CreatePlaylist, FetchContent, PopulatePlaylist
from security.user import get_current_user


router = APIRouter(prefix='/playlist', tags=['playlist'])


@router.post('/')
async def create_playlist(request: CreatePlaylist, current_user = Depends(get_current_user)):
    return await playlist.create_playlist(request.name, current_user)


@router.post('/content')
async def get_playlist_content(request: FetchContent, current_user = Depends(get_current_user)):
    return await playlist.get_playlist_content(request.playlist_id)


@router.post('/add-song')
async def add_song_to_playlist(request: PopulatePlaylist):
    return await playlist.add_song(request.song_id, request.playlist_id)


@router.post('/remove-song')
async def remove_song_from_playlist(request: PopulatePlaylist):
    return await playlist.remove_song(request.song_id, request.playlist_id)