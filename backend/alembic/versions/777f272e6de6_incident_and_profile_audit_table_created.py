"""incident and profile_audit table created

Revision ID: 777f272e6de6
Revises: 65c7229f930b
Create Date: 2026-08-10 08:23:58.286538
"""

from collections.abc import Sequence

import geoalchemy2
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers
revision: str = "777f272e6de6"
down_revision: str | Sequence[str] | None = "65c7229f930b"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "profile_audits",
        sa.Column("profile_id", sa.Uuid(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("phone_no", sa.String(), nullable=True),
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
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # safe index creation
    conn = op.get_bind()
    res = conn.execute(
        sa.text("SELECT to_regclass('idx_profile_audits_location')")
    ).scalar()
    if res is None:
        op.create_index(
            "idx_profile_audits_location",
            "profile_audits",
            ["location"],
            unique=False,
            postgresql_using="gist",
        )

    op.create_table(
        "incidents",
        sa.Column("heading", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("user_profile_id", sa.UUID(), nullable=True),
        sa.Column(
            "priority",
            sa.Enum("HIGH", "MEDIUM", "CRITICAL", name="priority"),
            nullable=False,
        ),
        sa.Column(
            "incident_category",
            postgresql.ENUM(
                "RESCUE",
                "MEDICAL",
                "SHELTER",
                "FOOD",
                "OTHERS",
                name="incident_category",
            ),
            nullable=False,
        ),
        sa.Column("location_description", sa.String(), nullable=False),
        sa.Column(
            "location",
            geoalchemy2.types.Geography(
                geometry_type="POINT",
                srid=4326,
                dimension=2,
                from_text="ST_GeogFromText",
                name="geography",
            ),
            nullable=False,
        ),
        sa.Column("details", sa.JSON(), nullable=False),
        sa.Column("profile_audit_id", sa.UUID(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["profile_audit_id"], ["profile_audits.id"], ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(["user_profile_id"], ["profiles.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # safe index creation
    res = conn.execute(sa.text("SELECT to_regclass('idx_incidents_location')")).scalar()
    if res is None:
        op.create_index(
            "idx_incidents_location",
            "incidents",
            ["location"],
            unique=False,
            postgresql_using="gist",
        )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("idx_incidents_location", table_name="incidents")
    op.drop_table("incidents")
    op.drop_index("idx_profile_audits_location", table_name="profile_audits")
    op.drop_table("profile_audits")
