from .config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{settings.postgres_username}:{settings.postgres_password}@{
    settings.postgres_hostname}:{settings.postgres_port}/{settings.postgres_name}"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
