from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class DbUser(Base):
    __tablename__ = 'users'
    uuid = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)

