from datetime import UTC, datetime

from app.ingestion.html_normalizer import HtmlDocumentNormalizer
from app.ingestion.raw_document import RawDocument


def test_html_normalizer_converts_html_to_plain_text() -> None:
    raw_document = RawDocument(
        source_identifier="w3c-wai-news",
        external_identifier="w3c-example-001",
        title="  W3C publishes accessibility guidance  ",
        url="https://www.w3.org/WAI/example",
        retrieved_at=datetime.now(UTC),
        raw_content="<p>Example <strong>accessibility</strong> guidance.</p>",
        metadata={"content_type": "text/html"},
    )

    normalizer = HtmlDocumentNormalizer()

    document = normalizer.normalize(raw_document)

    assert document.title == "W3C publishes accessibility guidance"
    assert document.plain_text == "Example accessibility guidance."
    assert document.canonical_url == raw_document.url
    assert document.content_hash is not None
    assert len(document.content_hash) == 64
    assert document.metadata == {"content_type": "text/html"}


def test_html_normalizer_handles_missing_content() -> None:
    raw_document = RawDocument(
        source_identifier="w3c-wai-news",
        external_identifier="w3c-example-002",
        title="Empty document",
        url="https://www.w3.org/WAI/empty",
        retrieved_at=datetime.now(UTC),
    )

    document = HtmlDocumentNormalizer().normalize(raw_document)

    assert document.plain_text == ""
    assert len(document.content_hash) == 64
