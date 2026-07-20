from datetime import UTC, datetime

from app.ingestion.normalized_document import NormalizedDocument
from app.ingestion.pipeline import IngestionPipeline
from app.ingestion.pipeline_stage import PipelineStage


class AppendTextStage(PipelineStage):
    def __init__(self, text: str) -> None:
        self._text = text

    def process(self, document: NormalizedDocument) -> NormalizedDocument:
        document.plain_text += self._text
        return document


def create_document() -> NormalizedDocument:
    return NormalizedDocument(
        source_identifier="w3c-wai-news",
        external_identifier="w3c-example-001",
        title="Accessibility guidance",
        canonical_url="https://www.w3.org/WAI/example",
        plain_text="Original",
        retrieved_at=datetime.now(UTC),
    )


def test_pipeline_runs_stages_in_order() -> None:
    pipeline = IngestionPipeline(
        stages=[
            AppendTextStage(" first"),
            AppendTextStage(" second"),
        ]
    )

    result = pipeline.process(create_document())

    assert result.plain_text == "Original first second"


def test_pipeline_without_stages_returns_document() -> None:
    document = create_document()

    result = IngestionPipeline().process(document)

    assert result is document


def test_pipeline_processes_multiple_documents() -> None:
    pipeline = IngestionPipeline(stages=[AppendTextStage(" processed")])

    results = pipeline.process_all([create_document(), create_document()])

    assert len(results) == 2
    assert all(result.plain_text.endswith(" processed") for result in results)
