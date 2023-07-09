from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from controllers import songs, auth, library, playlist, yt_search
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException
from database.postgresql import engine
from database.models import Base
import asyncio

from fastapi_jwt_auth import AuthJWT


app = FastAPI(title='Yumetune API')


app.include_router(songs.router)
app.include_router(auth.router)
app.include_router(library.router)
app.include_router(playlist.router)
app.include_router(yt_search.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['https://kotatsu.fun'],
    # allow_origins=['http://localhost:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


async def create_models(engine, Base):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.mount('/songs', StaticFiles(directory='/app/songs'), name='songs')
# app.mount('/songs', StaticFiles(directory='songs'), name='songs')

if __name__ == "__main__":
    asyncio.run(create_models(engine, Base))
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
