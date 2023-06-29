from pydantic import BaseModel


class CreatePlaylist(BaseModel):
    name: str


class FetchContent(BaseModel):
    playlist_id: int


class PopulatePlaylist(BaseModel):
    playlist_id: int
    song_id: int