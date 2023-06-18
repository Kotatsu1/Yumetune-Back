from fastapi import APIRouter, Depends
from controllers.stream import upload_song, songs
from controllers.auth.protect import get_current_user

router = APIRouter(prefix='/api/stream', tags=['stream'])


@router.post('/create')
async def upload_music(music_file = Depends(upload_song.create_hls_stream), current_user = Depends(get_current_user)):
    return music_file


@router.get('/all')
async def get_all_music(idk=Depends(songs.fetch_songs_from_db), current_user = Depends(get_current_user)):
    return idk