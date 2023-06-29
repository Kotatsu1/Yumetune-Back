from fastapi import APIRouter, Depends
from services import auth
from schemas.auth_schema import UserRegister, UserLogin


router = APIRouter(prefix='/auth', tags=['auth'])

@router.post('/register')
async def create_user(request: UserRegister):
    return await auth.create_user(request)


@router.post('/login')
async def login(di = Depends(auth.login)):
    return di


@router.post('/refresh')
async def refresh(di = Depends(auth.refresh)):
    return di


@router.delete('/logout')
async def logout(di = Depends(auth.logout)):
    return di