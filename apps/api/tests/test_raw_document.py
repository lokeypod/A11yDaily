from datetime import UTC, datetime

from app.ingestion.raw_document import RawDocument


def test_raw_document_stores_source_content() -> None:
    retrieved_at = datetime.now(UTC)

    document = RawDocument(
        source_identifier="w3c-wai-news",
        external_identifier="example-entry-1",
        title="Accessibility guidance published",
        url="https://example.com/accessibility-guidance",
        retrieved_at=retrieved_at,
        source_summary="Original publisher summary.",
    )

    assert document.source_identifier == "w3c-wai-news"
    assert document.external_identifier == "example-entry-1"
    assert document.source_summary == "Original publisher summary."
    assert document.metadata == {}
