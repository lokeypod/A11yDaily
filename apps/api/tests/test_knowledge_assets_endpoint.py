from fastapi.testclient import TestClient

from app.api.dependencies import get_knowledge_asset_repository
from app.domain.knowledge_asset import KnowledgeAsset
from app.main import app
from app.repositories.knowledge_assets_repository import (
    KnowledgeAssetRepository,
)


class FakeKnowledgeAssetRepository(KnowledgeAssetRepository):
    def __init__(self) -> None:
        self.last_offset: int | None = None
        self.last_limit: int | None = None

    def get_by_content_hash(
        self,
        content_hash: str,
    ) -> KnowledgeAsset | None:
        return None

    def find_recent(
        self,
        *,
        offset: int = 0,
        limit: int = 20,
        query: str | None = None,
    ) -> list[KnowledgeAsset]:
        self.last_offset = offset
        self.last_limit = limit

        return []

    def count(
        self,
        *,
        query: str | None = None,
    ) -> int:
        return 0

    def save(
        self,
        knowledge_asset: KnowledgeAsset,
    ) -> KnowledgeAsset:
        return knowledge_asset


fake_repository = FakeKnowledgeAssetRepository()


def override_knowledge_asset_repository() -> KnowledgeAssetRepository:
    return fake_repository


app.dependency_overrides[get_knowledge_asset_repository] = (
    override_knowledge_asset_repository
)

client = TestClient(app)


def test_knowledge_assets_endpoint_returns_paginated_response() -> None:
    response = client.get("/knowledge-assets")

    assert response.status_code == 200

    body = response.json()

    assert body["items"] == []
    assert body["page"] == 1
    assert body["page_size"] == 20
    assert body["total"] == 0


def test_knowledge_assets_endpoint_applies_pagination() -> None:
    response = client.get(
        "/knowledge-assets",
        params={
            "page": 3,
            "page_size": 5,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["page"] == 3
    assert body["page_size"] == 5
    assert fake_repository.last_offset == 10
    assert fake_repository.last_limit == 5
