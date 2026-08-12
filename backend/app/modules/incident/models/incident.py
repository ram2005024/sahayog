import uuid
from enum import Enum
from typing import TYPE_CHECKING

from geoalchemy2 import Geography
from sqlalchemy import JSON, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_user_model import BaseUserModel

if TYPE_CHECKING:
    from app.modules.auth.models.profiles.citizen_profile import Profile
    from app.modules.auth.models.profiles.profile_audit import ProfileAudit
    from app.modules.incident.models.incident_media import IncidentMedia


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


class IncidentStatus(str, Enum):
    PENDING = "pending"
    RESOLVED = "resolved"
    EN_ROUTE = "enroute"
    ARRIVED = "arrived"


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
    incident_status: Mapped[IncidentStatus] = mapped_column(
        ENUM(IncidentStatus, name="incident_status"), default=IncidentStatus.PENDING
    )
    location_description: Mapped[str]
    location: Mapped[str] = mapped_column(Geography(geometry_type="POINT", srid=4326))
    details: Mapped[dict] = mapped_column(JSON(), default=dict)
    profile_audit_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("profile_audits.id", ondelete="SET NULL"), nullable=True
    )

    # SQL ALCHEMY FIELDS
    reported_by: Mapped["Profile|None"] = relationship(
        "Profile", back_populates="registered_incidents"
    )
    profile_audit: Mapped["ProfileAudit|None"] = relationship(
        "ProfileAudit", back_populates="incidents"
    )  # Exists when the user is even deleted
    incident_medias: Mapped["IncidentMedia"] = relationship(
        "incident_medias.id",
        back_populates="incident",
        uselist=False,
        cascade="all,delete-orphan",
    )
