import asyncio
import logging

from app.config.settings import CONTENT_SOURCES_PATH
from app.config.source_registry import SourceRegistry
from app.ingestion.configured_ingestion_service import (
    ConfiguredIngestionService,
)
from app.logging_config import configure_logging

logger = logging.getLogger(__name__)


async def main() -> None:
    configure_logging()

    registry = SourceRegistry.load(CONTENT_SOURCES_PATH)
    service = ConfiguredIngestionService(registry)

    logger.info("Starting configured-source ingestion")
    await service.ingest_all()
    logger.info("Configured-source ingestion completed")


if __name__ == "__main__":
    asyncio.run(main())
