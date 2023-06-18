from fastapi import APIRouter, Depends
from controllers.stream import making_m3u8


router = APIRouter(prefix='/api/stream', tags=['stream'])


@router.post('/create')
async def upload_music(music_file = Depends(making_m3u8.create_hls_stream)):
    return music_file
