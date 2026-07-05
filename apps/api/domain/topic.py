from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True)
class Topic:
    """Represents a subject area that knowledge can relate to."""

    id: UUID
    name: str
    slug: str
    description: str | None = None