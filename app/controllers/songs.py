from fastapi import APIRouter, File, UploadFile, Body, Depends
from services import songs
from schemas.song_schema import Song
from security.user import get_current_user


router = APIRouter(prefix='/songs', tags=['songs'])


@router.post('/upload')
async def upload_song(artist = Body(...), title = Body(...), input_file: UploadFile = File(...), current_user = Depends(get_current_user)):
    return await songs.create_hls_stream(artist, title, input_file)


@router.get('/all')
async def list_songs():
    return await songs.fetch_songs_from_db()