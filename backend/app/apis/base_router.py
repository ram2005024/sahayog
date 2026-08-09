from fastapi import FastAPI

from app.apis.health_router import health_router


def include_base_router(app: FastAPI):
    app.include_router(health_router)
