from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_knowledge_asset_repository
from app.api.schemas.knowledge_asset import (
    KnowledgeAssetListResponse,
    KnowledgeAssetResponse,
)
from app.repositories.knowledge_assets_repository import (
    KnowledgeAssetRepository,
)

router = APIRouter(
    prefix="/knowledge-assets",
    tags=["Knowledge Assets"],
)


@router.get(
    "",
    response_model=KnowledgeAssetListResponse,
)
def list_knowledge_assets(
    repository: Annotated[
        KnowledgeAssetRepository,
        Depends(get_knowledge_asset_repository),
    ],
    page: int = Query(
        default=1,
        ge=1,
        description="Page number, beginning with 1.",
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
        description="Number of items returned per page.",
    ),
    q: str | None = Query(
        default=None,
        min_length=1,
        max_length=200,
        description="Search term matched against titles and summaries.",
    ),
) -> KnowledgeAssetListResponse:
    offset = (page - 1) * page_size

    assets = repository.find_recent(
        offset=offset,
        limit=page_size,
        query=q,
    )
    total = repository.count(
        query=q,
    )

    return KnowledgeAssetListResponse(
        items=[
            KnowledgeAssetResponse(
                id=asset.id,
                title=asset.title,
                url=asset.url,
                published_at=asset.published_at,
                summary=asset.summary,
            )
            for asset in assets
        ],
        page=page,
        page_size=page_size,
        total=total,
    )
