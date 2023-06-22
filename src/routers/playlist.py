from fastapi import APIRouter, Depends
from controllers.user import playlist


router = APIRouter(prefix='/api/playlist', tags=['playlist'])



@router.post('/create')
async def create_playlist(idk=Depends(playlist.create_playlist)):
    return idk


# @router.get('/all')
# async def get_user_library(idk=Depends(library.get_user_library)):
#     return idk


@router.post('/add')
async def add_song(idk=Depends(playlist.add_song)):
    return idk


# @router.post('/remove')
# async def remove_song(idk=Depends(library.remove_song)):
#     return idk