import asyncio
import logging

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
from app.persistence.repositories.sqlalchemy_source_repository import (
    SqlAlchemySourceRepository,
)

logger = logging.getLogger(__name__)


async def main() -> None:
    configure_logging()

    pipeline = IngestionPipeline(
        stages=[
            ContentHashStage(),
        ]
    )

    ingestion_service = IngestionService(
        pipeline=pipeline,
    )

    with SessionLocal() as session:
        source_repository = SqlAlchemySourceRepository(
            session=session,
        )

        knowledge_asset_repository = SqlAlchemyKnowledgeAssetRepository(
            session=session,
        )

        persistence_service = KnowledgeAssetPersistenceService(
            repository=knowledge_asset_repository,
        )

        service = ConfiguredIngestionService(
            source_repository=source_repository,
            ingestion_service=ingestion_service,
            persistence_service=persistence_service,
        )

        logger.info("Starting persisted-source ingestion")
        await service.ingest_all()
        logger.info("Persisted-source ingestion completed")


if __name__ == "__main__":
    asyncio.run(main())
