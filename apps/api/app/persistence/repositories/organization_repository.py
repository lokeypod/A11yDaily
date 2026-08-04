from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.organization import Organization


class OrganizationRepository(ABC):
    """Repository contract for organizations."""

    @abstractmethod
    def get_by_id(
        self,
        organization_id: UUID,
    ) -> Organization | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_name(
        self,
        name: str,
    ) -> Organization | None:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[Organization]:
        """Return all organizations."""
        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        organization: Organization,
    ) -> Organization:
        raise NotImplementedError
