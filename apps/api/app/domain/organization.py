from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True)
class Organization:
    """Represents an organization that publishes accessibility knowledge."""

    id: UUID
    name: str
    website: str
    description: str | None = None

    # Platform metadata
    authority_score: int = 100
    verified: bool = True