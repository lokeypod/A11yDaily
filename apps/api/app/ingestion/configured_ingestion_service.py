import logging

from app.config.source_registry import SourceRegistry
from app.ingestion.adapter_factory import AdapterFactory
from app.ingestion.html_normalizer import HtmlDocumentNormalizer
from app.ingestion.ingestion_service import IngestionService

logger = logging.getLogger(__name__)


class ConfiguredIngestionService:
    """Runs ingestion for every enabled configured source."""

    def __init__(
        self,
        registry: SourceRegistry,
        ingestion_service: IngestionService | None = None,
    ) -> None:
        self._registry = registry
        self._ingestion_service = ingestion_service or IngestionService()

    async def ingest_all(self) -> None:
        normalizer = HtmlDocumentNormalizer()

        for source in self._registry.enabled_sources():
            logger.info("Starting ingestion for source: %s", source.name)

            try:
                adapter = AdapterFactory.create(source)
                documents = await self._ingestion_service.ingest(
                    adapter=adapter,
                    normalizer=normalizer,
                )
            except Exception:
                logger.exception(
                    "Ingestion failed for source: %s",
                    source.name,
                )
                continue

            logger.info(
                "Processed %d documents from source: %s",
                len(documents),
                source.name,
            )
