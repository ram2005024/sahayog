from contextlib import asynccontextmanager

import redis.asyncio as aioredis
from fastapi import FastAPI

from app.core.config import settings


@asynccontextmanager
async def startup_redis(app: FastAPI):
    app.state.redis = aioredis.Redis(
        host=settings.REDIS_HOST,
        db=settings.REDIS_DB_NUMBER,
        port=settings.REDIS_PORT,
        decode_responses=True,
    )
    yield
    await app.state.redis.close()
