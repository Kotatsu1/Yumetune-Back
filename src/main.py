from fastapi import FastAPI
import uvicorn
from config import config
from fastapi.middleware.cors import CORSMiddleware
from auth.auth_router import auth_router
from users.user_router import user_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=config.CORS_METHODS,
    allow_headers=config.CORS_HEADERS,
)

app.include_router(auth_router)
app.include_router(user_router)


@app.get('/hello')
def hello_world():
    return "Hello, world!"


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000)
