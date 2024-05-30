from typing import List, Optional
from fastapi import APIRouter, Depends, Response, Request
from .user_models import UserModel
from .user_schemas import  User, UserUpdate
from .user_service import UserService
from auth.auth_service import AuthService
from security.auth_info import get_current_user, get_current_superuser, get_current_active_user

user_router = APIRouter(prefix="/users", tags=["user"])

@user_router.get("")
async def get_users_list(
    offset: Optional[int] = 0,
    limit: Optional[int] = 100,
    current_user: UserModel = Depends(get_current_superuser)
) -> List[User]:
    return await UserService.get_users_list(offset=offset, limit=limit)


@user_router.get("/me")
async def get_current_user(
    current_user: UserModel = Depends(get_current_active_user)
) -> User:
    return await UserService.get_user(current_user.id)


@user_router.put("/me")
async def update_current_user(
    user: UserUpdate,
    current_user: UserModel = Depends(get_current_user)
) -> User:
    return await UserService.update_user(current_user.id, user)


@user_router.delete("/me")
async def delete_current_user(
    request: Request,
    response: Response,
    current_user: UserModel = Depends(get_current_user)
):
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')

    await AuthService.logout(request.cookies.get('refresh_token'))
    await UserService.delete_user(current_user.id)
    return {"message": "User status is not active already"}


@user_router.get("/{user_id}")
async def get_user(
    user_id: str,
    current_user: UserModel = Depends(get_current_superuser)
) -> User:
    return await UserService.get_user(user_id)


@user_router.put("/{user_id}")
async def update_user(
    user_id: str,
    user: User,
    current_user: UserModel = Depends(get_current_superuser)
) -> User:
    return await UserService.update_user_from_superuser(user_id, user)


@user_router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    current_user: UserModel = Depends(get_current_superuser)
):
    await UserService.delete_user_from_superuser(user_id)
    return {"message": "User was deleted"}
