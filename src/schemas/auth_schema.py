from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class User(BaseModel):
    username: str
    password: str

class Settings(BaseModel):
    authjwt_secret_key: str = os.getenv("AUTHJWT_SECRET_KEY")
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_secure: bool = False
    authjwt_cookie_csrf_protect: bool = False
    # authjwt_cookie_samesite: str = 'lax'
