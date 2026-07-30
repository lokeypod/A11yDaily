from abc import ABC, abstractmethod

from app.domain.knowledge_asset import KnowledgeAsset


class KnowledgeAssetRepository(ABC):
    """Repository contract for knowledge assets."""

    @abstractmethod
    def get_by_content_hash(
        self,
        content_hash: str,
    ) -> KnowledgeAsset | None:
        raise NotImplementedError

    @abstractmethod
    def find_recent(
        self,
        *,
        offset: int = 0,
        limit: int = 20,
    ) -> list[KnowledgeAsset]:
        """Return recent knowledge assets with pagination."""
        raise NotImplementedError

    @abstractmethod
    def count(self) -> int:
        """Return the total number of knowledge assets."""
        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        knowledge_asset: KnowledgeAsset,
    ) -> KnowledgeAsset:
        raise NotImplementedError
