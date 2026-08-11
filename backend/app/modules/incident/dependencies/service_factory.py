# Incident service

from typing import Annotated

import redis.asyncio as aioredis
from fastapi import Depends

from app.dependencies.service_factories import get_redis_service
from app.modules.incident.dependencies.repo_factory import get_incident_repo
from app.modules.incident.repos.incident_repo import IncidentRepo
from app.modules.incident.services.incident_idempotancy_service import (
    IncidentIdempotancyService,
)
from app.modules.incident.services.incident_service import IncidentService


def get_incident_service(
    incident_repo: Annotated[IncidentRepo, Depends(get_incident_repo)],
):
    return IncidentService(incident_repo)


def get_incident_idempotancy_service(
    redis: Annotated[aioredis.Redis, Depends(get_redis_service)],
):
    return IncidentIdempotancyService(redis)
