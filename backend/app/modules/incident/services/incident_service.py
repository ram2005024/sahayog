from uuid import UUID

from app.modules.incident.repos.incident_repo import IncidentRepo
from app.modules.incident.schemas.incident import (
    IncidentCreateSchema,
    IncidentWithMediaRequestSchema,
)
from app.schemas.media_schema import IncidentMediaSchema


class IncidentService:
    def __init__(self, incident_repo: IncidentRepo) -> None:
        self.incident_repo = incident_repo

    # Services will come here
    async def create_incident_service(self, data: IncidentCreateSchema):
        return await self.incident_repo.create_incident(data)

    async def save_incident_medias(
        self, data: IncidentWithMediaRequestSchema, incident_id: UUID
    ):
        if not data.medias:
            return None
        image_medias = []
        audio_media = []
        if len(data.medias) > 0:
            for item in data.medias:
                if item.type == "image":
                    image_medias.append(item)
                if item.type == "audio":
                    audio_media.append(item)
        if len(image_medias) > 0:
            await self.save_incident_image_medias(image_medias, incident_id)
        if len(audio_media) > 0:
            await self.save_incident_audio_media(audio_media[0], incident_id)
        return True

    async def save_incident_image_medias(
        self,
        image_media: list[IncidentMediaSchema],
        incident_id: UUID,
    ):
        image_media_data = await self.create_image_media_data(image_media, incident_id)
        await self.incident_repo.save_image_media(image_media_data)
        return True

    async def save_incident_audio_media(
        self,
        audio_media: IncidentMediaSchema,
        incident_id: UUID,
    ):
        audio_media_data = await self.create_audio_media_data(audio_media, incident_id)
        await self.incident_repo.save_audio_media(audio_media_data)
        return True

    async def create_image_media_data(
        self, data: list[IncidentMediaSchema], incident_id: UUID
    ):
        image_urls = []
        meta_data = []
        for media_data in data:
            image_urls.append(media_data.url)
            meta_data.append(media_data.meta_data.model_dump())
        image_media_data_for_model = {
            "incident_id": incident_id,
            "image_urls": image_urls,
            "type": "image",
            "meta_data": meta_data,
        }
        return image_media_data_for_model

    async def create_audio_media_data(
        self, data: IncidentMediaSchema, incident_id: UUID
    ):
        audio_media_data_for_model = {
            "incident_id": incident_id,
            "audio_url": data.url,
            "type": "audio",
            "meta_data": list[data.meta_data.model_dump()],
        }
        return audio_media_data_for_model
