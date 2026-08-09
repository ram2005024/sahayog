from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database URLs
    ASYNC_DATABASE_URL: str = ""
    SYNC_DATABASE_URL: str = ""
    # REDIS url
    REDIS_URL: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
