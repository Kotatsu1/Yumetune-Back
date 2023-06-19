from pydantic import BaseModel



class Library(BaseModel):
    song_id: int
    user_uuid: str