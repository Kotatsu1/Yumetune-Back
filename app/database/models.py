from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class UserModel(Base):
    __tablename__ = 'users'
    uuid = Column(String, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)


class Songs(Base):
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True, index=True)
    artist = Column(String)
    title = Column(String)
    length = Column(Integer)


class UserLibrary(Base):
    __tablename__ = 'library'
    library_id = Column(Integer, primary_key=True, index=True)
    song_id = Column(Integer, ForeignKey('songs.id'))
    play_count = Column(Integer)
    added_at = Column(DateTime)
    user_uuid = Column(String, ForeignKey('users.uuid'))


class Playlist(Base):
    __tablename__ = 'playlists'
    playlist_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    user_uuid = Column(String, ForeignKey('users.uuid'))


class PlaylistContent(Base):
    __tablename__ = 'playlist_content'
    playlist_content_id = Column(Integer, primary_key=True, index=True)
    song_id = Column(Integer, ForeignKey('songs.id'))
    fk_playlist_id = Column(Integer, ForeignKey('playlists.playlist_id'))
