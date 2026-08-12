import cloudinary
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
    # Cloudinary
    CLOUD_NAME: str = ""
    CLOUD_SECRET: str = ""
    CLOUD_KEY: str = ""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

# Redis configuration
r = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB_NUMBER
)
# Cloudinary configuration
cloudinary = cloudinary.config(
    cloud_name=settings.CLOUD_NAME,
    api_key=settings.CLOUD_KEY,
    api_secret=settings.CLOUD_SECRET,
)
