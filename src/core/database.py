from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.core.config import get_settings

setting = get_settings()
engine = create_async_engine(setting.database_url, pool_pre_ping=True)
Session = async_sessionmaker(engine, expire_on_commit=False)
