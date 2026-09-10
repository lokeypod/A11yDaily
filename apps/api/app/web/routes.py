from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.api.dependencies import get_knowledge_asset_repository
from app.repositories.knowledge_assets_repository import (
    KnowledgeAssetRepository,
)

router = APIRouter()

templates = Jinja2Templates(
    directory="app/web/templates",
)


@router.get(
    "/",
    response_class=HTMLResponse,
)
def feed(
    request: Request,
    repository: Annotated[
        KnowledgeAssetRepository,
        Depends(get_knowledge_asset_repository),
    ],
) -> HTMLResponse:
    assets = repository.find_recent(
        offset=0,
        limit=100,
    )

    total = repository.count()

    return templates.TemplateResponse(
        request=request,
        name="feed.html",
        context={
            "assets": assets,
            "total": total,
        },
    )
