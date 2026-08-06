from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.source import Source


class SourceRepository(ABC):
    """Repository contract for sources."""

    @abstractmethod
    def get_by_id(
        self,
        source_id: UUID,
    ) -> Source | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_name(
        self,
        name: str,
    ) -> Source | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_organization_id(
        self,
        organization_id: UUID,
    ) -> list[Source]:
        """Return sources belonging to an organization."""
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[Source]:
        """Return all sources."""
        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        source: Source,
    ) -> Source:
        raise NotImplementedError
