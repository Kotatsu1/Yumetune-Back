from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os


load_dotenv()


engine = create_async_engine(
    os.getenv("POSTGRES_URL"),
    echo=True,
    future=True,
)


def async_session_generator():
    return sessionmaker(engine, class_=AsyncSession)


@asynccontextmanager
async def get_session():
    try:
        async_session = async_session_generator()

        async with async_session() as session:
            yield session
    except:
        await session.rollback()
        raise
    finally:
        await session.close()

