from pydantic import BaseModel


class UploadYT(BaseModel):
    source: str
    artist: str
    title: str