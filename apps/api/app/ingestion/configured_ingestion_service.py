import logging

from app.domain.source import SourceHealthStatus
from app.ingestion.adapter_factory import AdapterFactory
from app.ingestion.html_normalizer import HtmlDocumentNormalizer
from app.ingestion.ingestion_service import IngestionService
from app.ingestion.knowledge_asset_persistence_service import (
    KnowledgeAssetPersistenceService,
)
from app.repositories.source_repository import SourceRepository

logger = logging.getLogger(__name__)


class ConfiguredIngestionService:
    """Run ingestion and persistence for all active sources."""

    def __init__(
        self,
        source_repository: SourceRepository,
        ingestion_service: IngestionService,
        persistence_service: KnowledgeAssetPersistenceService,
    ) -> None:
        self._source_repository = source_repository
        self._ingestion_service = ingestion_service
        self._persistence_service = persistence_service

    async def ingest_all(self) -> None:
        normalizer = HtmlDocumentNormalizer()

        for source in self._source_repository.get_all():
            if not source.active:
                continue

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
                source.health_status = SourceHealthStatus.DEGRADED
                self._source_repository.update(source)

                logger.exception(
                    "Ingestion failed for source: %s",
                    source.name,
                )
                continue

            source.health_status = SourceHealthStatus.HEALTHY
            self._source_repository.update(source)

            logger.info(
                "Processed %d documents and saved %d new assets " "from source: %s",
                len(documents),
                len(saved_assets),
                source.name,
            )
