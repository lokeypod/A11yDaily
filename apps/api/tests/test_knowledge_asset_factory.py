from datetime import UTC, datetime

from app.ingestion.knowledge_asset_factory import KnowledgeAssetFactory
from app.ingestion.normalized_document import NormalizedDocument


def test_factory_creates_knowledge_asset() -> None:
    published_at = datetime(2026, 7, 1, tzinfo=UTC)
    retrieved_at = datetime(2026, 7, 20, tzinfo=UTC)

    document = NormalizedDocument(
        source_identifier="w3c-wai-news",
        external_identifier="w3c-example-001",
        title="W3C publishes accessibility guidance",
        canonical_url="https://www.w3.org/WAI/example",
        plain_text="Example accessibility guidance.",
        retrieved_at=retrieved_at,
        published_at=published_at,
        source_summary="Original publisher summary.",
        content_hash="example-hash",
    )

    asset = KnowledgeAssetFactory().create(document)

    assert asset.title == document.title
    assert asset.url == document.canonical_url
    assert asset.published_at == published_at
    assert asset.discovered_at == retrieved_at
    assert asset.summary == "Original publisher summary."
    assert asset.ai_summary is None
    assert asset.content_hash == "example-hash"


def test_factory_uses_retrieved_time_when_publish_date_is_missing() -> None:
    retrieved_at = datetime(2026, 7, 20, tzinfo=UTC)

    document = NormalizedDocument(
        source_identifier="w3c-wai-news",
        external_identifier="w3c-example-002",
        title="Accessibility update",
        canonical_url="https://www.w3.org/WAI/update",
        plain_text="Accessibility update.",
        retrieved_at=retrieved_at,
    )

    asset = KnowledgeAssetFactory().create(document)

    assert asset.published_at == retrieved_at
