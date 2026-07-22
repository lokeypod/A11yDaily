from datetime import UTC, datetime

from app.ingestion.normalized_document import NormalizedDocument


def test_normalized_document_defaults_metadata() -> None:
    document = NormalizedDocument(
        source_identifier="w3c-wai-news",
        external_identifier="w3c-example-001",
        title="Accessibility guidance",
        canonical_url="https://www.w3.org/WAI/example",
        plain_text="Example accessibility guidance.",
        retrieved_at=datetime.now(UTC),
    )

    assert document.metadata == {}
    assert document.content_hash is None
