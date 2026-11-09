import os

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://asifbabur@127.0.0.1:5432/supportflow_dev",
)


class Base(DeclarativeBase):
    pass


engine = create_async_engine(DATABASE_URL)
Session = async_sessionmaker(engine)
