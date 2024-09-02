from typing import Optional
from fastapi import APIRouter, Depends
from .user_models import UserModel
from .user_schemas import  User, UserUpdate
from .user_service import UserService
from security.auth_info import get_current_user, get_current_superuser

user_router = APIRouter(prefix="/users", tags=["user"])

@user_router.get("")
async def get_users_list(
    offset: Optional[int] = 0,
    limit: Optional[int] = 100,
    current_user: UserModel = Depends(get_current_superuser)
) -> list[User]:
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
    await UserService.delete_user(user_id)
    return {"message": "User was deleted"}
