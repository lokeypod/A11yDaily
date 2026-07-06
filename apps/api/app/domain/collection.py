from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True)
class Collection:
    id: UUID