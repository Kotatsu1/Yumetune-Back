from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_jwt_auth import AuthJWT
from schemas.auth_schema import Settings, UserLogin
from typing import Annotated
from controllers.auth import signup
from controllers.auth.hashing import Hash
from utils.db.db import get_session
from controllers.db.models import UserModel
from sqlalchemy import select, or_
from datetime import timedelta


router = APIRouter(prefix='/api/auth', tags=['auth'])


@AuthJWT.load_config
def get_config():
    return Settings()


@router.post('/register')
async def register(user: Annotated[dict, Depends(signup.create_user)]):
    return user


@router.post('/login')
async def login(request: UserLogin, Authorize: AuthJWT = Depends()):

    if request.login:
        async with get_session() as session:
            stmt = select(UserModel).filter(or_(UserModel.username == request.login, UserModel.email == request.login))
            result = await session.execute(stmt)
            user = result.scalars().first()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Login not provided')

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Invalid credentials')
    
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Incorrect password')
    

    access_token = Authorize.create_access_token(subject=user.uuid, expires_time=timedelta(minutes=30))
    refresh_token = Authorize.create_refresh_token(subject=user.uuid, expires_time=timedelta(days=30))


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


async def get_current_user(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    return current_user

