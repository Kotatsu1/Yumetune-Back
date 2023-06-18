from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UserModel(Base):
    __tablename__ = 'users'
    uuid = Column(String, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)


class Songs(Base):
    __tablename__ = 'songs'
    id = Column(String, primary_key=True, index=True)
    artist = Column(String)
    title = Column(String)


class UserLibrary(Base):
    __tablename__ = 'library'
    id = Column(String, primary_key=True, index=True)
    title = Column(String)
    play_count = Column(Integer)
    added_at = Column(DateTime)
    user_uuid = Column(String, ForeignKey('users.uuid'))
