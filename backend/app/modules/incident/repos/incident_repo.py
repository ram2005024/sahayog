from geoalchemy2.shape import from_shape
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.incident.models.incident import Incident
from app.modules.incident.schemas.incident import IncidentCreateSchema


class IncidentRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    # incident repos will come here
    async def create_incident(self, data: IncidentCreateSchema):
        to_put_data = data.model_dump(
            exclude={"latitude", "longitude"}, exclude_unset=True
        )
        to_put_data["incident_category"] = data.details.type
        to_put_data["location"] = from_shape(data.location, srid=4326)
        new_data = Incident()
        for key, value in to_put_data.items():
            setattr(new_data, key, value)
        self.db.add(new_data)
        await self.db.flush()
        await self.db.commit()
        new_data = (
            await self.db.execute(select(Incident).where(Incident.id == new_data.id))
        ).scalar_one_or_none()
        return new_data
