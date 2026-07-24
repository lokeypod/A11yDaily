from fastapi.testclient import TestClient

from app.api.dependencies import get_knowledge_asset_repository
from app.domain.knowledge_asset import KnowledgeAsset
from app.main import app
from app.repositories.knowledge_assets_repository import (
    KnowledgeAssetRepository,
)


class FakeKnowledgeAssetRepository(KnowledgeAssetRepository):
    """In-memory repository used for API endpoint tests."""

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
    ) -> list[KnowledgeAsset]:
        return []

    def count(self) -> int:
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


def test_list_knowledge_assets_returns_paginated_response() -> None:
    response = client.get("/knowledge-assets")

    assert response.status_code == 200
    assert response.json() == {
        "items": [],
        "page": 1,
        "page_size": 20,
        "total": 0,
    }


def test_list_knowledge_assets_accepts_pagination_parameters() -> None:
    response = client.get(
        "/knowledge-assets",
        params={
            "page": 2,
            "page_size": 5,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "items": [],
        "page": 2,
        "page_size": 5,
        "total": 0,
    }


def test_list_knowledge_assets_rejects_page_zero() -> None:
    response = client.get(
        "/knowledge-assets",
        params={"page": 0},
    )

    assert response.status_code == 422


def test_list_knowledge_assets_rejects_excessive_page_size() -> None:
    response = client.get(
        "/knowledge-assets",
        params={"page_size": 101},
    )

    assert response.status_code == 422
