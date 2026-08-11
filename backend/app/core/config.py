import redis
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database URLs
    ASYNC_DATABASE_URL: str = ""
    SYNC_DATABASE_URL: str = ""
    # REDIS
    REDIS_URL: str = ""
    REDIS_HOST: str = ""
    REDIS_PORT: int = 6379
    REDIS_DB_NUMBER: int = 0

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

# Redis configuration
r = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB_NUMBER
)
