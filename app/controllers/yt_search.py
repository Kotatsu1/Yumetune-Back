from fastapi import APIRouter
from services import yt_search
from schemas.yt_upload_schema import UploadYT



router = APIRouter(prefix='/yt_search', tags=['yt_search'])


@router.get('/search')
def search_songs(request: str):
    return yt_search.search_yt(request)


@router.post('/create_hls')
async def create_hls_from_yt(request: UploadYT):
    return await yt_search.create_hls_from_yt(request.source, request.artist, request.title)