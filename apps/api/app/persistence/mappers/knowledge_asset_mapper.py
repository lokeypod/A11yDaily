from app.domain.knowledge_asset import KnowledgeAsset
from app.persistence.models.knowledge_asset import KnowledgeAssetModel


class KnowledgeAssetMapper:
    """Convert between domain and persistence representations."""

    @staticmethod
    def to_model(asset: KnowledgeAsset) -> KnowledgeAssetModel:
        return KnowledgeAssetModel(
            id=asset.id,
            title=asset.title,
            url=asset.url,
            published_at=asset.published_at,
            discovered_at=asset.discovered_at,
            summary=asset.summary,
            ai_summary=asset.ai_summary,
            content_hash=asset.content_hash,
        )

    @staticmethod
    def to_domain(model: KnowledgeAssetModel) -> KnowledgeAsset:
        return KnowledgeAsset(
            id=model.id,
            title=model.title,
            url=model.url,
            published_at=model.published_at,
            discovered_at=model.discovered_at,
            summary=model.summary,
            ai_summary=model.ai_summary,
            content_hash=model.content_hash,
        )
