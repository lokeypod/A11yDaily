from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True)
class Story:
    id: UUID