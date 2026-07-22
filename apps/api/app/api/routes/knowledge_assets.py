from fastapi import APIRouter

from app.api.schemas.knowledge_asset import KnowledgeAssetResponse
from app.database.session import SessionLocal
from app.persistence.repositories.sqlalchemy_knowledge_asset_repository import (
    SqlAlchemyKnowledgeAssetRepository,
)

router = APIRouter(
    prefix="/knowledge-assets",
    tags=["Knowledge Assets"],
)


@router.get(
    "",
    response_model=list[KnowledgeAssetResponse],
)
def list_knowledge_assets() -> list[KnowledgeAssetResponse]:
    with SessionLocal() as session:
        repository = SqlAlchemyKnowledgeAssetRepository(session)
        assets = repository.get_recent()

    return [
        KnowledgeAssetResponse(
            id=asset.id,
            title=asset.title,
            url=asset.url,
            published_at=asset.published_at,
            summary=asset.summary,
        )
        for asset in assets
    ]
