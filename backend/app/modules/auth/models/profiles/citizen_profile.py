import uuid
from typing import TYPE_CHECKING

from geoalchemy2 import Geography
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_user_model import BaseUserModel

if TYPE_CHECKING:
    from app.modules.auth.models.user import User
    from app.modules.incident.models.incident import Incident


class Profile(BaseUserModel):
    __tablename__ = "profiles"
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    first_name: Mapped[str]
    last_name: Mapped[str | None]
    total_registered_incidents: Mapped[int] = mapped_column(default=0)
    picture: Mapped[str | None]
    location: Mapped[str | None] = mapped_column(
        Geography(geometry_type="POINT", srid=4326)
    )
    location_description: Mapped[str | None]
    emergency_phone_no: Mapped[str | None]
    user: Mapped["User"] = relationship("User", back_populates="profile")
    registerd_incidents: Mapped[list["Incident"] | None] = relationship(
        "Incident", cascade="all,delete-orphan"
    )
