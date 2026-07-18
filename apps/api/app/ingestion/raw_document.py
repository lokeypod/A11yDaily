from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class RawDocument:
    """Unprocessed content retrieved from a public source."""

    source_identifier: str
    external_identifier: str
    title: str
    url: str

    retrieved_at: datetime
    published_at: datetime | None = None

    raw_content: str | None = None
    source_summary: str | None = None
    author: str | None = None
    language: str | None = None

    metadata: dict[str, Any] = field(default_factory=dict)
