import logging

from app.config.source_registry import SourceRegistry
from app.ingestion.adapter_factory import AdapterFactory
from app.ingestion.html_normalizer import HtmlDocumentNormalizer
from app.ingestion.ingestion_service import IngestionService
from app.ingestion.knowledge_asset_persistence_service import (
    KnowledgeAssetPersistenceService,
)

logger = logging.getLogger(__name__)


class ConfiguredIngestionService:
    """Run ingestion and persistence for all enabled configured sources."""

    def __init__(
        self,
        registry: SourceRegistry,
        ingestion_service: IngestionService,
        persistence_service: KnowledgeAssetPersistenceService,
    ) -> None:
        self._registry = registry
        self._ingestion_service = ingestion_service
        self._persistence_service = persistence_service

    async def ingest_all(self) -> None:
        normalizer = HtmlDocumentNormalizer()

        for source in self._registry.enabled_sources():
            logger.info(
                "Starting ingestion for source: %s",
                source.name,
            )

            try:
                adapter = AdapterFactory.create(source)

                documents = await self._ingestion_service.ingest(
                    adapter=adapter,
                    normalizer=normalizer,
                )

                saved_assets = self._persistence_service.persist(
                    documents,
                )
            except Exception:
                logger.exception(
                    "Ingestion failed for source: %s",
                    source.name,
                )
                continue

            logger.info(
                "Processed %d documents and saved %d new assets from source: %s",
                len(documents),
                len(saved_assets),
                source.name,
            )
