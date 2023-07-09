from fastapi import APIRouter
from services import yt_search



router = APIRouter(prefix='/yt_search', tags=['yt_search'])


@router.get('/search')
def search_songs(request: str):
    return yt_search.search_yt(request)