from fastapi import FastAPI

from app.apis.health_router import health_router
from app.apis.media_router import media_api as media_api_v1
from app.modules.incident.api.v1.incident_api import (
    incident_router as incident_router_v1,
)


def include_base_router(app: FastAPI):
    # Basics
    app.include_router(health_router)

    # Incident module
    app.include_router(incident_router_v1, prefix="/api/v1")
    app.include_router(media_api_v1)
