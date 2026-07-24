from collections.abc import Generator

from app.database.session import SessionLocal
from app.persistence.repositories.sqlalchemy_knowledge_asset_repository import (
    SqlAlchemyKnowledgeAssetRepository,
)
from app.repositories.knowledge_assets_repository import (
    KnowledgeAssetRepository,
)


def get_knowledge_asset_repository() -> Generator[KnowledgeAssetRepository, None, None]:
    with SessionLocal() as session:
        yield SqlAlchemyKnowledgeAssetRepository(session)
