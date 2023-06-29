from pydantic import BaseModel


class Song(BaseModel):
    artist: str
    title: str
    