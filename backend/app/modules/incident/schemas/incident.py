from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from app.modules.incident.models.incident import Priority
from app.modules.incident.schemas.annotation import Details
from app.schemas.media_schema import IncidentMediaSchema


class IncidentWithMediaRequestSchema(BaseModel):
    heading: str
    description: str | None = None
    user_profile_id: str | None = None
    priority: Priority
    location_description: str
    latitude: float
    longitude: float
    details: Annotated[Details, Field(discriminator="type")]
    medias: list[IncidentMediaSchema] | None = None

    @field_validator("latitude", "longitude", mode="before")
    def normalize_lat_long(cls, val):
        return float(val)

    @field_validator("user_profile_id", mode="before")
    def empty_str_to_none(cls, v):
        if v == "":
            return None
        return v


class IncidentCreateSchema(BaseModel):
    heading: str
    description: str | None = None
    user_profile_id: str | None = None
    priority: Priority
    location_description: str
    latitude: float
    longitude: float
    details: Annotated[Details, Field(discriminator="type")]

    @field_validator("user_profile_id", mode="before")
    def empty_str_to_none(cls, v):
        if v == "":
            return None
        return v

    @field_validator("latitude", "longitude", mode="before")
    def normalize_lat_long(cls, val):
        return float(val)


class IncidentReadBasic(BaseModel):
    id: UUID
    heading: str
    description: str
    priority: Priority
    location_description: str
    details: dict
