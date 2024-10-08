from typing import Optional
import uuid
from jose import jwt
from fastapi import Depends, HTTPException, status
from users.user_models import UserModel
from utils import OAuth2PasswordBearerWithCookie
from users.user_service import UserService
from auth.exceptions import InvalidTokenException
from config import config

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/auth/signin")


async def get_current_user(
        token: str = Depends(oauth2_scheme)
) -> Optional[UserModel]:
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if user_id is None:
            raise InvalidTokenException
    except Exception:
        raise InvalidTokenException

    current_user = await UserService.get_user(uuid.UUID(user_id))

    return current_user


async def get_current_superuser(current_user: UserModel = Depends(get_current_user)) -> UserModel:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough privileges")
    return current_user
