from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseModel):
    authjwt_secret_key: str = os.getenv("AUTHJWT_SECRET_KEY")
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_secure: bool = True
    authjwt_cookie_csrf_protect: bool = False
    authjwt_cookie_samesite: str = 'lax'


class UserRegister(BaseModel):
    username: str
    email: str
    password: str

        
class UserLogin(BaseModel):
    login: str
    password: str
