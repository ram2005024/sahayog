"""added incident status field in incident model

Revision ID: 1fc868403f9a
Revises: 777f272e6de6
Create Date: 2026-08-11 05:50:02.401230
"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1fc868403f9a"
down_revision: str | Sequence[str] | None = "777f272e6de6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create enum type first
    incident_status_enum = postgresql.ENUM(
        "PENDING",
        "RESOLVED",
        "EN_ROUTE",
        "ARRIVED",
        name="incident_status",
        create_type=True,
    )
    incident_status_enum.create(op.get_bind(), checkfirst=True)

    # Add column using the enum type
    op.add_column(
        "incidents", sa.Column("incident_status", incident_status_enum, nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop column first
    op.drop_column("incidents", "incident_status")

    # Drop enum type
    incident_status_enum = postgresql.ENUM(name="incident_status")
    incident_status_enum.drop(op.get_bind(), checkfirst=True)
