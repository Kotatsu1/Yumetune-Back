from fastapi import APIRouter, Depends
from controllers.user import library


router = APIRouter(prefix='/api/library', tags=['library'])


@router.get('/all')
async def get_user_library(idk=Depends(library.get_user_library)):
    return idk


@router.post('/add')
async def add_song(idk=Depends(library.add_song)):
    return idk


@router.post('/remove')
async def remove_song(idk=Depends(library.remove_song)):
    return idk