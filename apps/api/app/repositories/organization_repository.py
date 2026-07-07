from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.organization import Organization


class OrganizationRepository(ABC):
    """Repository interface for Organization entities."""

    @abstractmethod
    def get_all(self) -> list[Organization]:
        """Return all organizations."""
        raise NotImplementedError

    @abstractmethod
    def get(self, organization_id: UUID) -> Organization | None:
        """Return an organization by ID."""
        raise NotImplementedError

    @abstractmethod
    def create(self, organization: Organization) -> Organization:
        """Persist a new organization."""
        raise NotImplementedError