# Different category schemas
# For rescue
from typing import Literal

from pydantic import BaseModel, computed_field

from app.modules.incident.models.incident import IncidentCategory


class RescueSchema(BaseModel):
    type: Literal[IncidentCategory.RESCUE]
    no_of_peoples_affected: int
    no_of_volunteers_required: int = 1
    life_threat: bool = False

    @computed_field
    @property
    def is_team_required(self) -> bool:
        return self.no_of_volunteers_required > 5


class MedicalSchema(BaseModel):
    type: Literal[IncidentCategory.MEDICAL]
    ambulance_required: bool = False
    doctors_required: bool = False
    life_threat: bool = False
    blood_required: bool = False


class ShelterSchema(BaseModel):
    type: Literal[IncidentCategory.SHELTER]
    has_family: bool = False
    no_of_people: int = 1


class FoodSchema(BaseModel):
    type: Literal[IncidentCategory.FOOD]
    no_of_people: int = 1
    has_elders: bool = False


class OthersSchema(BaseModel):
    type: Literal[IncidentCategory.OTHERS]
    no_of_people_affected: int = 1
    life_threat: bool = False
