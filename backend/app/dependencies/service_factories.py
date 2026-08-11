import redis.asyncio as aioredis
from fastapi import Request


def get_redis_service(request: Request) -> aioredis.Redis:
    return request.app.state.redis
