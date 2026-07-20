import pytest

from app.ingestion.adapters.static_w3c import StaticW3CAdapter
from app.ingestion.html_normalizer import HtmlDocumentNormalizer
from app.ingestion.ingestion_service import IngestionService
from app.ingestion.normalized_document import NormalizedDocument
from app.ingestion.pipeline import IngestionPipeline
from app.ingestion.pipeline_stage import PipelineStage


class AppendSourceStage(PipelineStage):
    def process(self, document: NormalizedDocument) -> NormalizedDocument:
        document.plain_text += " Processed by pipeline."
        return document


@pytest.mark.asyncio
async def test_ingestion_service_fetches_normalizes_and_processes_documents() -> None:
    pipeline = IngestionPipeline(stages=[AppendSourceStage()])
    service = IngestionService(pipeline=pipeline)

    documents = await service.ingest(
        adapter=StaticW3CAdapter(),
        normalizer=HtmlDocumentNormalizer(),
    )

    assert len(documents) == 1

    document = documents[0]

    assert document.title == "W3C publishes accessibility guidance"
    assert document.source_identifier == "w3c-wai-news"
    assert document.plain_text == (
        "Example accessibility guidance. Processed by pipeline."
    )
    assert len(document.content_hash) == 64
