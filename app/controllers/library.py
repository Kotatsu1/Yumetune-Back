from fastapi import APIRouter, Depends
from services import library
from schemas.library_schema import Library
from security.user import get_current_user

router = APIRouter(prefix='/library', tags=['library'])



@router.get('/')
async def get_user_library(current_user = Depends(get_current_user)):
    return await library.get_user_library(current_user)


@router.post('/add')
async def add_song_to_library(request: Library, current_user = Depends(get_current_user)):
    return await library.add_song(request, current_user)


@router.post('/remove')
async def remove_song_from_library(request: Library, current_user = Depends(get_current_user)):
    return await library.remove_song(request, current_user)