from fastapi import APIRouter, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT
from schemas.auth_schema import Settings, User

router = APIRouter(prefix='/api/auth', tags=['auth'])


@AuthJWT.load_config
def get_config():
    return Settings()


@router.post('/login')
def login(user: User, Authorize: AuthJWT = Depends()):

    if user.username != "test" or user.password != "test":
        raise HTTPException(status_code=401,detail="Bad username or password")


    access_token = Authorize.create_access_token(subject=user.username)
    refresh_token = Authorize.create_refresh_token(subject=user.username)


    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    return {"msg":"Successfully login"}

@router.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)

    Authorize.set_access_cookies(new_access_token)
    return {"msg":"The token has been refresh"}

@router.delete('/logout')
def logout(Authorize: AuthJWT = Depends()):

    Authorize.jwt_required()

    Authorize.unset_jwt_cookies()
    return {"msg":"Successfully logout"}

@router.get('/protected')
def protected(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}