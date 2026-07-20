from uuid import uuid4

from app.domain.knowledge_asset import KnowledgeAsset
from app.ingestion.normalized_document import NormalizedDocument


class KnowledgeAssetFactory:
    """Create domain knowledge assets from normalized documents."""

    def create(self, document: NormalizedDocument) -> KnowledgeAsset:
        return KnowledgeAsset(
            id=uuid4(),
            title=document.title,
            url=document.canonical_url,
            published_at=document.published_at or document.retrieved_at,
            discovered_at=document.retrieved_at,
            summary=document.source_summary,
            content_hash=document.content_hash,
        )
