from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from messenger.settings import settings


url = URL.create(
    "postgresql+asyncpg",
    settings.postgres_username,
    settings.postgres_password,
    settings.postgres_host,
    settings.postgres_port,
)

engine = create_async_engine(url, connect_args={}, echo=True)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
