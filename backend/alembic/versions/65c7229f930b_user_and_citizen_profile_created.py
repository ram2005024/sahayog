"""user and citizen profile created

Revision ID: 65c7229f930b
Revises:
Create Date: 2026-08-10 06:54:52.085256
"""

from collections.abc import Sequence

import geoalchemy2
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "65c7229f930b"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column(
            "role",
            sa.ARRAY(
                postgresql.ENUM(
                    "CITIZEN", "VOLUNTEER", "COORDINATOR", "ADMIN", name="user_roles"
                )
            ),
            nullable=False,
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("phone_no", sa.String(), nullable=True),
        sa.Column("hashed_password", sa.String(), nullable=True),
        sa.Column(
            "provider",
            postgresql.ENUM("MANUAL", "GOOGLE", "FACEBOOK", name="login_providers"),
            nullable=False,
        ),
        sa.Column("provider_id", sa.String(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("provider_id"),
    )
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)

    op.create_table(
        "profiles",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("total_registered_incidents", sa.Integer(), nullable=False),
        sa.Column("picture", sa.String(), nullable=True),
        sa.Column(
            "location",
            geoalchemy2.types.Geography(
                geometry_type="POINT",
                srid=4326,
                dimension=2,
                from_text="ST_GeogFromText",
                name="geography",
            ),
            nullable=True,
        ),
        sa.Column("location_description", sa.String(), nullable=True),
        sa.Column("emergency_phone_no", sa.String(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # only create index if it doesn't already exist
    conn = op.get_bind()
    res = conn.execute(sa.text("SELECT to_regclass('idx_profiles_location')")).scalar()
    if res is None:
        op.create_index(
            "idx_profiles_location",
            "profiles",
            ["location"],
            unique=False,
            postgresql_using="gist",
        )


def downgrade() -> None:
    """Downgrade schema."""
    op.create_table(
        "spatial_ref_sys",
        sa.Column("srid", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column(
            "auth_name", sa.VARCHAR(length=256), autoincrement=False, nullable=True
        ),
        sa.Column("auth_srid", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column(
            "srtext", sa.VARCHAR(length=2048), autoincrement=False, nullable=True
        ),
        sa.Column(
            "proj4text", sa.VARCHAR(length=2048), autoincrement=False, nullable=True
        ),
        sa.CheckConstraint(
            "srid > 0 AND srid <= 998999", name=op.f("spatial_ref_sys_srid_check")
        ),
        sa.PrimaryKeyConstraint("srid", name=op.f("spatial_ref_sys_pkey")),
    )
    op.drop_index(
        "idx_profiles_location", table_name="profiles", postgresql_using="gist"
    )
    op.drop_table("profiles")
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_table("users")
