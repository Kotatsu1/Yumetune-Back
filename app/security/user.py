from fastapi_jwt_auth import AuthJWT
from fastapi import Depends, HTTPException



async def get_current_user(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

    current_user = Authorize.get_jwt_subject()
    return current_user

