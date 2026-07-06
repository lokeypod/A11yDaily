from dataclasses import dataclass
from enum import Enum
from uuid import UUID


class SourceType(str, Enum):
    STANDARDS = "standards"
    GOVERNMENT = "government"
    LEGAL = "legal"
    BLOG = "blog"
    NEWS = "news"
    COMMUNITY = "community"
    VIDEO = "video"
    OPEN_SOURCE = "open_source"
    DOCUMENT_ACCESSIBILITY = "document_accessibility"
    RESEARCH = "research"
    VENDOR = "vendor"


class ConnectorType(str, Enum):
    RSS = "rss"
    API = "api"
    SCRAPER = "scraper"
    MANUAL = "manual"


@dataclass(slots=True)
class Source:
    """Represents a public source where A11yDaily discovers knowledge."""

    id: UUID
    organization_id: UUID
    name: str
    url: str
    source_type: SourceType
    connector_type: ConnectorType
    authority_score: int = 50
    active: bool = True
    refresh_minutes: int = 60
    description: str | None = None