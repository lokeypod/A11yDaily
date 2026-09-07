"""add source empty result telemetry

Revision ID: 4adb53d4d739
Revises: 44b760f1737d
Create Date: 2026-09-07 23:14:53.789685
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4adb53d4d739"
down_revision: str | Sequence[str] | None = "44b760f1737d"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "sources",
        sa.Column(
            "consecutive_empty_results",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    op.alter_column(
        "sources",
        "consecutive_empty_results",
        server_default=None,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(
        "sources",
        "consecutive_empty_results",
    )
