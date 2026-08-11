from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, model_validator
from shapely.geometry import Point

from app.modules.incident.models.incident import Priority
from app.modules.incident.schemas.annotation import Details


class IncidentCreateSchema(BaseModel):
    heading: str
    description: str | None = None
    user_profile_id: str | None = None
    priority: Priority
    location_description: str
    latitude: float
    longitude: float
    details: Annotated[Details, Field(discriminator="type")]

    location: Point | None = Field(default=None, exclude=True)

    model_config = {"arbitrary_types_allowed": True}

    @field_validator("latitude", "longitude", mode="before")
    def normalize_lat_long(cls, val):
        return float(val)

    @model_validator(mode="after")
    def add_location(self):
        self.location = Point(self.longitude, self.latitude)
        return self


class IncidentReadBasic(BaseModel):
    id: UUID
    heading: str
    description: str
    priority: Priority
    location_description: str
    details: dict
