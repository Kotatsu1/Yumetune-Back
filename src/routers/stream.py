from fastapi import APIRouter, Depends
from controllers.stream import upload_song, songs


router = APIRouter(prefix='/api/stream', tags=['stream'])


@router.post('/create')
async def upload_music(music_file = Depends(upload_song.create_hls_stream)):
    return music_file


@router.get('/all')
async def get_all_music(idk=Depends(songs.fetch_songs_from_db)):
    return idk