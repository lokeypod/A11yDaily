import logging

from app.domain.knowledge_asset import KnowledgeAsset
from app.ingestion.knowledge_asset_factory import KnowledgeAssetFactory
from app.ingestion.normalized_document import NormalizedDocument
from app.repositories.knowledge_assets_repository import (
    KnowledgeAssetRepository,
)

logger = logging.getLogger(__name__)


class KnowledgeAssetPersistenceService:
    """Create and persist new knowledge assets from normalized documents."""

    def __init__(
        self,
        repository: KnowledgeAssetRepository,
        factory: KnowledgeAssetFactory | None = None,
    ) -> None:
        self._repository = repository
        self._factory = factory or KnowledgeAssetFactory()

    def persist(
        self,
        documents: list[NormalizedDocument],
    ) -> list[KnowledgeAsset]:
        saved_assets: list[KnowledgeAsset] = []

        for document in documents:
            if not document.content_hash:
                logger.warning(
                    "Skipping document without content hash: %s",
                    document.canonical_url,
                )
                continue

            existing_asset = self._repository.get_by_content_hash(document.content_hash)

            if existing_asset is not None:
                logger.info(
                    "Skipping duplicate knowledge asset: %s",
                    document.canonical_url,
                )
                continue

            asset = self._factory.create(document)
            saved_assets.append(self._repository.save(asset))

        return saved_assets
