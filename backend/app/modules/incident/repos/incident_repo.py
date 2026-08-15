from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.incident.models.incident import Incident
from app.modules.incident.models.incident_media import IncidentMedia
from app.modules.incident.schemas.incident import IncidentCreateSchema


class IncidentRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    # incident repos will come here
    async def create_incident(self, data: IncidentCreateSchema):
        location = Point(data.longitude, data.latitude)
        to_put_data = data.model_dump(
            exclude={"latitude", "longitude"}, exclude_unset=True
        )
        to_put_data["location"] = from_shape(location, srid=4326)
        to_put_data["incident_category"] = data.details.type

        new_data = Incident()
        for key, value in to_put_data.items():
            setattr(new_data, key, value)
        self.db.add(new_data)
        await self.db.flush()
        await self.db.commit()
        return new_data

    async def save_image_media(self, data):
        to_put = IncidentMedia(**data)
        self.db.add(to_put)
        await self.db.commit()
        return True

    async def save_audio_media(self, data):
        to_put = IncidentMedia(**data)
        self.db.add(to_put)
        await self.db.commit()
        return True
