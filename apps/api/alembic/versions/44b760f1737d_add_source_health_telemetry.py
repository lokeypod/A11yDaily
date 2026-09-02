"""add source health telemetry

Revision ID: 44b760f1737d
Revises: 399e1b5b7c24
Create Date: 2026-09-02 20:57:29.480363
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "44b760f1737d"
down_revision: str | Sequence[str] | None = "399e1b5b7c24"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "sources",
        sa.Column(
            "last_attempt_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    op.add_column(
        "sources",
        sa.Column(
            "last_success_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    op.add_column(
        "sources",
        sa.Column(
            "consecutive_failures",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    op.alter_column(
        "sources",
        "consecutive_failures",
        server_default=None,
    )

    op.add_column(
        "sources",
        sa.Column(
            "last_error",
            sa.Text(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(
        "sources",
        "last_error",
    )
    op.drop_column(
        "sources",
        "consecutive_failures",
    )
    op.drop_column(
        "sources",
        "last_success_at",
    )
    op.drop_column(
        "sources",
        "last_attempt_at",
    )
