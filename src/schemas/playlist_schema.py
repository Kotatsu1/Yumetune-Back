from pydantic import BaseModel


class CreatePlaylist(BaseModel):
    name: str


class ManagePlaylist(BaseModel):
    song_id: int
    playlist_id: int