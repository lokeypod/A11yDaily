from abc import ABC, abstractmethod

from app.domain.knowledge_asset import KnowledgeAsset


class KnowledgeAssetRepository(ABC):
    """Repository contract for KnowledgeAssets."""

    @abstractmethod
    def get_by_content_hash(
        self,
        content_hash: str,
    ) -> KnowledgeAsset | None:
        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        knowledge_asset: KnowledgeAsset,
    ) -> KnowledgeAsset:
        raise NotImplementedError
