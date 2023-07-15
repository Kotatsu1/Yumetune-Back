from fastapi import HTTPException, status, Depends
import uuid
from security.hashing import Hash
from database.postgresql import get_session
from database.models import UserModel
from sqlalchemy import select, or_
from schemas.auth_schema import UserRegister, UserLogin
from fastapi_jwt_auth import AuthJWT
from datetime import timedelta
from schemas.auth_schema import Settings


@AuthJWT.load_config
def get_config():
    return Settings()



async def create_user(request: UserRegister):
    async with get_session() as session:
        stmt = select(UserModel).filter(or_(UserModel.username == request.username, UserModel.email == request.email))
        result = await session.execute(stmt)
        existing_user = result.scalars().first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'User already exists')


        new_user = UserModel(
            uuid = str(uuid.uuid4()),
            username = request.username,
            email = request.email,
            password = Hash.bcrypt(request.password)
        )

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
    return new_user
    

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
    

    access_token = Authorize.create_access_token(subject=user.uuid, expires_time=timedelta(minutes=15))
    refresh_token = Authorize.create_refresh_token(subject=user.uuid, expires_time=timedelta(days=30))


    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    return {"msg":"Successfully login"}


async def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user, expires_time=timedelta(minutes=15))

    Authorize.set_access_cookies(new_access_token)
    return {"msg":"The token has been refresh"}


async def logout(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()

        Authorize.unset_jwt_cookies()
        return {"msg":"Successfully logout"}
    
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))