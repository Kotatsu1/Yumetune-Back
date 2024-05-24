from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from argparse import ArgumentParser
from config import config

parser = ArgumentParser()
parser.add_argument("-m", "--mode")

mode = parser.parse_args().mode

config.set_mode(mode)
config.update_config()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=config.CORS_METHODS,
    allow_headers=config.CORS_HEADERS,
)

@app.get('/hello')
def hello_world():
    return "Hello, world!"


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
