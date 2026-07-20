import pytest

from app.ingestion.adapters.static_w3c import StaticW3CAdapter
from app.ingestion.html_normalizer import HtmlDocumentNormalizer
from app.ingestion.ingestion_service import IngestionService


@pytest.mark.asyncio
async def test_ingestion_service_fetches_and_normalizes_documents() -> None:
    service = IngestionService()

    documents = await service.ingest(
        adapter=StaticW3CAdapter(),
        normalizer=HtmlDocumentNormalizer(),
    )

    assert len(documents) == 1

    document = documents[0]

    assert document.title == "W3C publishes accessibility guidance"
    assert document.plain_text == "Example accessibility guidance."
    assert document.source_identifier == "w3c-wai-news"
    assert len(document.content_hash) == 64
