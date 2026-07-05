from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class KnowledgeAsset:
    """A single piece of publicly available accessibility knowledge."""

    id: UUID

    title: str
    url: str

    published_at: datetime
    discovered_at: datetime

    summary: str | None = None
    ai_summary: str | None = None

    content_hash: str | None = None
