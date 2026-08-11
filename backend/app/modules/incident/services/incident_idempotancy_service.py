import redis.asyncio as aioredis


class IncidentIdempotancyService:
    def __init__(
        self,
        redis: aioredis.Redis,
    ) -> None:
        self.redis = redis
        self.incident_key_lifetime = 10  # In mins

    async def check_incident_key(self, key: str):
        return await self.redis.exists(f"incident:{key}:created")

    async def check_request_key(self, key):
        return await self.redis.exists(f"incident:{key}:locked")

    async def acquire_lock(self, key):
        return await self.redis.set(f"incident:{key}:locked", "1", nx=True, px=5000)

    async def set_idempotancy_incident_key(self, key: str):
        return await self.redis.set(
            f"incident:{key}:created", "1", ex=self.incident_key_lifetime * 60
        )

    async def delete_lock_key(self, key: str):
        return await self.redis.delete(f"incident:{key}:locked")
