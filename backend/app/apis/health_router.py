from fastapi import APIRouter
from redis import asyncio as aioredis
from sqlalchemy import text

from app.core.config import settings
from app.core.db import engine

health_router = APIRouter()


@health_router.get("/health")
async def get_health_status():
    status = {}
    try:
        async with engine.connect() as db:
            await db.execute(text("SELECT 1"))
            status["database"] = "ok"
    except Exception as e:  # noqa: BLE001
        status["database"] = f"error:{e}"

    try:
        redis = await aioredis.from_url(settings.REDIS_URL)
        await redis.ping()
        await redis.close()
        status["redis"] = "ok"
    except Exception as e:  # noqa: BLE001
        status["redis"] = f"error-{e}"
    return status
