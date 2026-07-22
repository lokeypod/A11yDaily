from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class NormalizedDocument:
    """Canonical document representation used inside A11yDaily."""

    source_identifier: str
    external_identifier: str

    title: str
    canonical_url: str
    plain_text: str

    retrieved_at: datetime
    published_at: datetime | None = None

    source_summary: str | None = None
    author: str | None = None
    language: str | None = None

    content_hash: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
