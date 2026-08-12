import asyncio
from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies.get_user import get_user
from app.modules.incident.dependencies.incident import get_idempotancy_key
from app.modules.incident.dependencies.service_factory import (
    get_incident_idempotancy_service,
    get_incident_service,
)
from app.modules.incident.schemas.incident import (
    IncidentCreateSchema,
    IncidentReadBasic,
)
from app.modules.incident.services.incident_idempotancy_service import (
    IncidentIdempotancyService,
)
from app.modules.incident.services.incident_service import IncidentService
from app.schemas.common import SuccessResponse

incident_router = APIRouter(prefix="/sos/incident", tags=["Incident apis"])


# CREATE INCIDENT
@incident_router.post("/", response_model=SuccessResponse[IncidentReadBasic])
async def create_incident_endpoint(
    data: IncidentCreateSchema,
    key: Annotated[
        str,
        Depends(get_idempotancy_key),
    ],
    user: Annotated[str, Depends(get_user)],
    incident_service: Annotated[IncidentService, Depends(get_incident_service)],
    idempotancy_service: Annotated[
        IncidentIdempotancyService, Depends(get_incident_idempotancy_service)
    ],
):
    try:
        got_lock = await idempotancy_service.acquire_lock(key)
        if not got_lock:
            while await idempotancy_service.check_request_key(key):
                await asyncio.sleep(0.05)
        if await idempotancy_service.check_incident_key(key):
            return SuccessResponse(message="Already processed")
            # Create the incident
        incident = await incident_service.create_incident_service(data)
        await idempotancy_service.set_idempotancy_incident_key(key)
        return SuccessResponse(message="Incident created succssfuly", data=incident)
    finally:
        await idempotancy_service.delete_lock_key(key)
