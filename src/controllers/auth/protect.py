from fastapi_jwt_auth import AuthJWT
from fastapi import Depends


async def get_current_user(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    return current_user
