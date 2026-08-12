import uuid
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import ARRAY, JSON, TEXT, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_user_model import BaseUserModel

if TYPE_CHECKING:
    from app.modules.auth.models.profiles.citizen_profile import Profile
    from app.modules.auth.models.profiles.profile_audit import ProfileAudit
    from app.modules.incident.models.incident import Incident


class MediaTypes(str, Enum):
    IMAGE = "image"
    AUDIO = "audio"


class IncidentMedia(BaseUserModel):
    __tablename__ = "incident_medias"

    incident_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("incidents.id", ondelete="CASCADE"), index=True
    )
    image_urls: Mapped[list[str] | None] = mapped_column(ARRAY(TEXT), nullable=True)
    audio_url: Mapped[str | None]
    types: Mapped[list[MediaTypes]] = mapped_column(
        ARRAY(ENUM(MediaTypes, name="media_types_incident"))
    )
    uploaded_by_profile_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("profiles.id"), nullable=True
    )
    meta_data: Mapped[list[dict]] = mapped_column(ARRAY(JSON))
    profile_audit_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("profile_audits.id", ondelete="SET NULL"), nullable=True
    )
    # SQLALCHEMY fields
    incident: Mapped["Incident"] = relationship(
        "Incident", back_populates="incident_medias"
    )
    uploaded_by: Mapped["Profile"] = relationship(
        "Profile", back_populates="user_incident_images"
    )
    profile_audit: Mapped["ProfileAudit|None"] = relationship(
        "ProfileAudit", back_populates="incident_images"
    )  # Exists when the user is even deleted
