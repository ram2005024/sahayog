from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies.get_user import get_user
from app.schemas.media_schema import IncidentSignatureRequest
from app.services.cloudinary_service import CloudinaryService

media_api = APIRouter(prefix="/ap1/v1/incident/media")


@media_api.post("/signatures")
def get_media_signatures(
    data: IncidentSignatureRequest,
    user_id: Annotated[str, Depends(get_user)],  # User id is demo
    media_service: Annotated[CloudinaryService, Depends(CloudinaryService)],
):
    return media_service.generate_signatures_for_incident_medias(user_id, data)
