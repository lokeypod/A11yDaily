import hashlib

import pytest

from app.ingestion.adapters.static_w3c import StaticW3CAdapter
from app.ingestion.html_normalizer import HtmlDocumentNormalizer
from app.ingestion.ingestion_service import IngestionService
from app.ingestion.normalized_document import NormalizedDocument
from app.ingestion.pipeline import IngestionPipeline
from app.ingestion.pipeline_stage import PipelineStage
from app.ingestion.stages.content_hash import ContentHashStage


class AppendSourceStage(PipelineStage):
    def process(self, document: NormalizedDocument) -> NormalizedDocument:
        document.plain_text += " Processed by pipeline."
        return document


@pytest.mark.asyncio
async def test_ingestion_service_fetches_normalizes_and_processes_documents() -> None:
    pipeline = IngestionPipeline(
        stages=[
            AppendSourceStage(),
            ContentHashStage(),
        ]
    )
    service = IngestionService(pipeline=pipeline)

    documents = await service.ingest(
        adapter=StaticW3CAdapter(),
        normalizer=HtmlDocumentNormalizer(),
    )

    assert len(documents) == 1

    document = documents[0]
    expected_text = "Example accessibility guidance. Processed by pipeline."

    assert document.title == "W3C publishes accessibility guidance"
    assert document.source_identifier == "w3c-wai-news"
    assert document.plain_text == expected_text
    assert (
        document.content_hash
        == hashlib.sha256(expected_text.encode("utf-8")).hexdigest()
    )
