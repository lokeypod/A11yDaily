from datetime import UTC, datetime
from uuid import uuid4

import pytest
from bs4 import BeautifulSoup
from fastapi.testclient import TestClient

from app.api.dependencies import get_knowledge_asset_repository
from app.domain.knowledge_asset import KnowledgeAsset
from app.main import app


class FakeFeedRepository:
    def __init__(self, assets: list[KnowledgeAsset]) -> None:
        self.assets = assets

    def find_recent(
        self,
        *,
        offset: int = 0,
        limit: int = 100,
    ) -> list[KnowledgeAsset]:
        return self.assets[offset : offset + limit]

    def count(self) -> int:
        return len(self.assets)


client = TestClient(app)


def test_feed_page_loads(monkeypatch: pytest.MonkeyPatch) -> None:
    repository = FakeFeedRepository([])

    monkeypatch.setitem(
        app.dependency_overrides,
        get_knowledge_asset_repository,
        lambda: repository,
    )

    response = client.get("/")

    assert response.status_code == 200
    assert "A11yDaily" in response.text


def test_feed_displays_known_publication_date(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    asset = KnowledgeAsset(
        id=uuid4(),
        title="Accessibility news",
        url="https://example.com/news",
        published_at=datetime(2026, 11, 20, tzinfo=UTC),
        discovered_at=datetime(2026, 11, 22, tzinfo=UTC),
    )

    repository = FakeFeedRepository([asset])

    monkeypatch.setitem(
        app.dependency_overrides,
        get_knowledge_asset_repository,
        lambda: repository,
    )

    response = client.get("/")

    assert response.status_code == 200
    assert "Accessibility news" in response.text
    assert "Published:" in response.text
    assert "November 20, 2026" in response.text
    assert "Discovered:" not in response.text

    soup = BeautifulSoup(response.text, "html.parser")
    time_element = soup.find("time")

    assert time_element is not None
    assert time_element["datetime"] == asset.published_at.isoformat()


def test_feed_displays_discovery_date_when_publication_is_unknown(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    asset = KnowledgeAsset(
        id=uuid4(),
        title="Accessibility resource",
        url="https://example.com/resource",
        published_at=None,
        discovered_at=datetime(2026, 11, 22, tzinfo=UTC),
    )

    repository = FakeFeedRepository([asset])

    monkeypatch.setitem(
        app.dependency_overrides,
        get_knowledge_asset_repository,
        lambda: repository,
    )

    response = client.get("/")

    assert response.status_code == 200
    assert "Accessibility resource" in response.text
    assert "Discovered:" in response.text
    assert "November 22, 2026" in response.text
    assert "Published:" not in response.text

    soup = BeautifulSoup(response.text, "html.parser")
    time_element = soup.find("time")

    assert time_element is not None
    assert time_element["datetime"] == asset.discovered_at.isoformat()