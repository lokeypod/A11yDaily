"""add source health status

Revision ID: 399e1b5b7c24
Revises: 91360d58ec2f
Create Date: 2026-09-02 01:08:06.667409
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "399e1b5b7c24"
down_revision: str | Sequence[str] | None = "91360d58ec2f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "sources",
        sa.Column(
            "health_status",
            sa.String(length=50),
            nullable=False,
            server_default="healthy",
        ),
    )

    op.alter_column(
        "sources",
        "health_status",
        server_default=None,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(
        "sources",
        "health_status",
    )
