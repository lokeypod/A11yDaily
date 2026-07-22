import asyncio
import logging

from app.config.settings import CONTENT_SOURCES_PATH
from app.config.source_registry import SourceRegistry
from app.database.session import SessionLocal
from app.ingestion.configured_ingestion_service import (
    ConfiguredIngestionService,
)
from app.ingestion.ingestion_service import IngestionService
from app.ingestion.knowledge_asset_persistence_service import (
    KnowledgeAssetPersistenceService,
)
from app.ingestion.pipeline import IngestionPipeline
from app.ingestion.stages.content_hash import ContentHashStage
from app.logging_config import configure_logging
from app.persistence.repositories.sqlalchemy_knowledge_asset_repository import (
    SqlAlchemyKnowledgeAssetRepository,
)

logger = logging.getLogger(__name__)


async def main() -> None:
    configure_logging()

    registry = SourceRegistry.load(CONTENT_SOURCES_PATH)

    pipeline = IngestionPipeline(
        stages=[
            ContentHashStage(),
        ]
    )

    ingestion_service = IngestionService(
        pipeline=pipeline,
    )

    with SessionLocal() as session:
        repository = SqlAlchemyKnowledgeAssetRepository(
            session=session,
        )

        persistence_service = KnowledgeAssetPersistenceService(
            repository=repository,
        )

        service = ConfiguredIngestionService(
            registry=registry,
            ingestion_service=ingestion_service,
            persistence_service=persistence_service,
        )

        logger.info("Starting configured-source ingestion")
        await service.ingest_all()
        logger.info("Configured-source ingestion completed")


if __name__ == "__main__":
    asyncio.run(main())
