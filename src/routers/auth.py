from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_jwt_auth import AuthJWT
from schemas.auth_schema import Settings, User
from typing import Annotated
from controllers.auth import signup

from controllers.auth.hashing import Hash
from utils.db.db import get_session
from controllers.db.models import UserModel
from sqlalchemy import select

router = APIRouter(prefix='/api/auth', tags=['auth'])


@AuthJWT.load_config
def get_config():
    return Settings()


@router.post('/register')
async def register(user: Annotated[dict, Depends(signup.create_user)]):
    return user


@router.post('/login')
async def login(request: User, Authorize: AuthJWT = Depends()):

    if request.username:
        async with get_session() as session:
            stmt = select(UserModel).filter(UserModel.username == request.username)
            result = await session.execute(stmt)
            user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Invalid credentials')
        
        if not Hash.verify(user.password, request.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Incorrect password')


    elif request.email:
        async with get_session() as session:
            stmt = select(UserModel).filter(UserModel.email == request.email)
            result = await session.execute(stmt)
            user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Invalid credentials')
        
        if not Hash.verify(user.password, request.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Incorrect password')


    access_token = Authorize.create_access_token(subject=request.username)
    refresh_token = Authorize.create_refresh_token(subject=request.username)


    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    return {"msg":"Successfully login"}

@router.post('/refresh')
async def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)

    Authorize.set_access_cookies(new_access_token)
    return {"msg":"The token has been refresh"}

@router.delete('/logout')
async def logout(Authorize: AuthJWT = Depends()):

    Authorize.jwt_required()

    Authorize.unset_jwt_cookies()
    return {"msg":"Successfully logout"}

@router.get('/protected')
async def protected(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}