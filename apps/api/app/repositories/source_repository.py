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
    def get_by_organization_id_and_name(
        self,
        organization_id: UUID,
        name: str,
    ) -> Source | None:
        """Return a source by organization and name."""
        raise NotImplementedError

    @abstractmethod
    def get_by_url(
        self,
        url: str,
    ) -> Source | None:
        """Return a source by its canonical URL."""
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
