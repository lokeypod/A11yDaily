from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class KnowledgeAssetResponse(BaseModel):
    id: UUID
    title: str
    url: str
    published_at: datetime | None
    summary: str | None


class KnowledgeAssetListResponse(BaseModel):
    items: list[KnowledgeAssetResponse]
    page: int = Field(ge=1)
    page_size: int = Field(ge=1)
    total: int = Field(ge=0)
