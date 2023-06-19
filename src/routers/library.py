from fastapi import APIRouter, Depends
from controllers.user import library


router = APIRouter(prefix='/api/library', tags=['library'])


@router.post('/all')
async def get_user_library(idk=Depends()):
    return idk


@router.post('/add')
async def add_song(idk=Depends(library.add_song)):
    return idk


@router.post('/remove')
async def remove_song(idk=Depends()):
    return idk