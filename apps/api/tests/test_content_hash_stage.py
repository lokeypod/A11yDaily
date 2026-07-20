import hashlib
from datetime import UTC, datetime

from app.ingestion.normalized_document import NormalizedDocument
from app.ingestion.stages.content_hash import ContentHashStage


def create_document(plain_text: str) -> NormalizedDocument:
    return NormalizedDocument(
        source_identifier="w3c-wai-news",
        external_identifier="w3c-example-001",
        title="Accessibility guidance",
        canonical_url="https://www.w3.org/WAI/example",
        plain_text=plain_text,
        retrieved_at=datetime.now(UTC),
    )


def test_content_hash_stage_calculates_hash() -> None:
    document = create_document("Example accessibility guidance.")

    result = ContentHashStage().process(document)

    expected_hash = hashlib.sha256(b"Example accessibility guidance.").hexdigest()

    assert result.content_hash == expected_hash


def test_content_hash_changes_when_content_changes() -> None:
    first_document = create_document("Original content.")
    second_document = create_document("Updated content.")

    stage = ContentHashStage()

    first_result = stage.process(first_document)
    second_result = stage.process(second_document)

    assert first_result.content_hash != second_result.content_hash
