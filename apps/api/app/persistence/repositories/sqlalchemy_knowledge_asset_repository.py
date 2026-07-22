from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.knowledge_asset import KnowledgeAsset
from app.persistence.mappers.knowledge_asset_mapper import (
    KnowledgeAssetMapper,
)
from app.persistence.models.knowledge_asset import KnowledgeAssetModel
from app.repositories.knowledge_assets_repository import (
    KnowledgeAssetRepository,
)


class SqlAlchemyKnowledgeAssetRepository(KnowledgeAssetRepository):
    """Persist knowledge assets using SQLAlchemy."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_content_hash(
        self,
        content_hash: str,
    ) -> KnowledgeAsset | None:
        statement = select(KnowledgeAssetModel).where(
            KnowledgeAssetModel.content_hash == content_hash
        )

        model = self._session.scalar(statement)

        if model is None:
            return None

        return KnowledgeAssetMapper.to_domain(model)

    def save(
        self,
        knowledge_asset: KnowledgeAsset,
    ) -> KnowledgeAsset:
        model = KnowledgeAssetMapper.to_model(knowledge_asset)

        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)

        return KnowledgeAssetMapper.to_domain(model)
