import uuid

from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class OrganizationModel(Base):
    """Database representation of an organization."""

    __tablename__ = "organizations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )

    website: Mapped[str] = mapped_column(
        String(2_000),
        nullable=False,
        unique=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    authority_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=100,
    )

    verified: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
