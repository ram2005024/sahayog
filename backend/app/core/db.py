from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

engine = create_async_engine(settings.ASYNC_DATABASE_URL, echo=True)

AsyncSessioLocal = async_sessionmaker(
    bind=engine, expire_on_commit=True, autoflush=False
)

# Base
Base = declarative_base()


# Db factory
async def get_async_db():
    async with AsyncSessioLocal() as db:
        try:
            yield db
        finally:
            await db.close()


sync_engine = create_engine(settings.SYNC_DATABASE_URL, echo=True)

SyncSessionLocal = sessionmaker(
    bind=sync_engine, autoflush=False, autocommit=False, expire_on_commit=True
)


async def get_sync_db():
    db = SyncSessionLocal()
    try:
        yield db
        db.close()
    except SQLAlchemyError:
        db.rollback()
    finally:
        db.close()
