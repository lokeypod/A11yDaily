import uuid

from sqlalchemy import Boolean, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.domain.source import ConnectorType, SourceType


class SourceModel(Base):
    """Database representation of a content source."""

    __tablename__ = "sources"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    url: Mapped[str] = mapped_column(
        String(2_000),
        nullable=False,
        unique=True,
    )

    source_type: Mapped[SourceType] = mapped_column(
        Enum(SourceType, name="source_type"),
        nullable=False,
    )

    connector_type: Mapped[ConnectorType] = mapped_column(
        Enum(ConnectorType, name="connector_type"),
        nullable=False,
    )

    authority_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=50,
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    refresh_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=60,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    health_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="healthy",
    )
