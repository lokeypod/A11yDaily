import pytest

from app.ingestion.adapters.static_w3c import StaticW3CAdapter


@pytest.mark.asyncio
async def test_static_w3c_adapter_returns_raw_document() -> None:
    adapter = StaticW3CAdapter()

    documents = await adapter.fetch()

    assert len(documents) == 1

    document = documents[0]

    assert document.source_identifier == "w3c-wai-news"
    assert document.external_identifier == "w3c-example-001"
    assert document.title == "W3C publishes accessibility guidance"
    assert document.language == "en"
    assert document.metadata["adapter"] == "static_w3c"
