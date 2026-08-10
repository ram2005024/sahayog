from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import ARRAY
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_user_model import BaseUserModel

if TYPE_CHECKING:
    from app.modules.auth.models.profiles.citizen_profile import Profile


# Role enums
class Role(str, Enum):
    CITIZEN = "citizen"
    VOLUNTEER = "volunteer"
    COORDINATOR = "coordinator"
    ADMIN = "admin"


class Providers(str, Enum):
    MANUAL = "manual"
    GOOGLE = "google"
    FACEBOOK = "facebook"


class User(BaseUserModel):
    __tablename__ = "users"
    role: Mapped[list[Role]] = mapped_column(
        ARRAY(ENUM(Role, name="user_roles")), default=lambda: [Role.CITIZEN]
    )
    is_active: Mapped[bool] = mapped_column(default=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True)
    phone_no: Mapped[str] = mapped_column(nullable=True)
    hashed_password: Mapped[str] = mapped_column(nullable=True)
    provider: Mapped[Providers] = mapped_column(
        ENUM(Providers, name="login_providers"), default=Providers.MANUAL
    )
    provider_id: Mapped[str] = mapped_column(unique=True, nullable=True)
    profile: Mapped["Profile"] = relationship(
        "Profile", back_populates="user", cascade="all,delete-orphan", uselist=False
    )
