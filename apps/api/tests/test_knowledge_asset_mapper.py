from datetime import UTC, datetime
from uuid import uuid4

from app.domain.knowledge_asset import KnowledgeAsset
from app.persistence.mappers.knowledge_asset_mapper import (
    KnowledgeAssetMapper,
)


def create_asset() -> KnowledgeAsset:
    return KnowledgeAsset(
        id=uuid4(),
        title="Accessible documents update",
        url="https://example.com/accessible-documents",
        published_at=datetime(2026, 7, 20, tzinfo=UTC),
        discovered_at=datetime(2026, 7, 21, tzinfo=UTC),
        summary="Publisher summary.",
        ai_summary=None,
        content_hash="a" * 64,
    )


def test_mapper_converts_domain_asset_to_model() -> None:
    asset = create_asset()

    model = KnowledgeAssetMapper.to_model(asset)

    assert model.id == asset.id
    assert model.title == asset.title
    assert model.url == asset.url
    assert model.content_hash == asset.content_hash


def test_mapper_converts_model_back_to_domain() -> None:
    asset = create_asset()
    model = KnowledgeAssetMapper.to_model(asset)

    result = KnowledgeAssetMapper.to_domain(model)

    assert result == asset
