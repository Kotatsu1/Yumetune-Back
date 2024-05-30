import uuid

from fastapi import APIRouter, Depends, Response, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from users.user_models import UserModel
from users.user_schemas import UserCreate, User
from .auth_schemas import Token
from .auth_service import AuthService
from users.user_service import UserService
from security.auth_info import get_current_user, get_current_active_user
from users.exceptions import InvalidCredentialsException
from config import config


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    user: UserCreate
) -> User:
    return await UserService.register_new_user(user)


@auth_router.post("/signin")
async def signin(
    response: Response,
    credentials: OAuth2PasswordRequestForm = Depends()
) -> Token:
    user = await AuthService.authenticate_user(credentials.username, credentials.password)
    if not user:
        raise InvalidCredentialsException
    token = await AuthService.create_token(user.id)
    response.set_cookie(
        'access_token',
        token.access_token,
        max_age=config.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        httponly=True
    )
    response.set_cookie(
        'refresh_token',
        token.refresh_token,
        max_age=config.REFRESH_TOKEN_EXPIRE_DAYS * 30 * 24 * 60,
        httponly=True
    )
    return token


@auth_router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    user: UserModel = Depends(get_current_active_user),
):
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')

    await AuthService.logout(request.cookies.get('refresh_token'))
    return {"message": "Logged out successfully"}


@auth_router.post("/refresh")
async def refresh_token(
    request: Request,
    response: Response
) -> Token:
    new_token = await AuthService.refresh_token(
        uuid.UUID(request.cookies.get("refresh_token"))
    )

    response.set_cookie(
        'access_token',
        new_token.access_token,
        max_age=config.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        httponly=True,
    )
    response.set_cookie(
        'refresh_token',
        new_token.refresh_token,
        max_age=config.REFRESH_TOKEN_EXPIRE_DAYS * 30 * 24 * 60,
        httponly=True,
    )
    return new_token


@auth_router.post("/abort")
async def abort_all_sessions(
    response: Response,
    user: UserModel = Depends(get_current_user)
):
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')

    await AuthService.abort_all_sessions(user.id)
    return {"message": "All sessions was aborted"}


