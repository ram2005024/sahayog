# Usually to backup the user info when they delete their account inside the incident table

import uuid
from typing import TYPE_CHECKING

from geoalchemy2 import Geography
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_user_model import BaseUserModel

if TYPE_CHECKING:
    from app.models import Incident


class ProfileAudit(BaseUserModel):
    __tablename__ = "profile_audits"
    profile_id: Mapped[uuid.UUID]
    username: Mapped[str]
    email: Mapped[str]
    phone_no: Mapped[str | None]
    picture: Mapped[str | None]
    location: Mapped[str | None] = mapped_column(
        Geography(geometry_type="POINT", srid=4326)
    )
    location_description: Mapped[str | None]
    first_name: Mapped[str]
    last_name: Mapped[str | None]
    incidents: Mapped[list["Incident"] | None] = relationship(
        "Incident", cascade="all", back_populates="profile_audit"
    )
