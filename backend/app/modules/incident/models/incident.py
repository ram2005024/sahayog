import uuid
from enum import Enum
from typing import TYPE_CHECKING

from geoalchemy2 import Geography
from sqlalchemy import JSON, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_user_model import BaseUserModel

if TYPE_CHECKING:
    from app.models import Profile


class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    CRITICAL = "critical"


class IncidentCategory(str, Enum):
    RESCUE = "rescue"
    MEDICAL = "medical"
    SHELTER = "shelter"
    FOOD = "food"
    OTHERS = "others"


class Incident(BaseUserModel):
    __tablename__ = "incidents"

    heading: Mapped[str]
    description: Mapped[str | None]
    user_profile_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("profiles.id"), nullable=True
    )
    priority: Mapped[Priority] = mapped_column(default=Priority.MEDIUM)
    incident_category: Mapped[IncidentCategory] = mapped_column(
        ENUM(IncidentCategory, name="incident_category")
    )
    location_description: Mapped[str]
    location: Mapped[str] = mapped_column(Geography(geometry_type="POINT", srid=4326))
    details: Mapped[dict] = mapped_column(JSON(), default=dict)
    profile_audit_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("profile_audits.id", ondelete="SET NULL"), nullable=True
    )
    reported_by: Mapped["Profile"] = relationship("Profile", back_populates="incident")
    profile_audit: Mapped["Profile|None"] = relationship(
        "profile_audits.id", back_populates="incidents"
    )  # Exists when the user is even deleted
