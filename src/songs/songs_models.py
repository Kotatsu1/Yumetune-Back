import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from database import Base

class SongModel(Base):
    __tablename__ = 'songs'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    artist: Mapped[str] = mapped_column()
    title: Mapped[str] = mapped_column()
    quality: Mapped[str] = mapped_column()
    duration: Mapped[int] = mapped_column()

