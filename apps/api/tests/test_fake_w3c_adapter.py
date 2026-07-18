import pytest

from app.ingestion.adapters.fake_w3c import FakeW3CAdapter


@pytest.mark.asyncio
async def test_fake_w3c_adapter_returns_raw_document() -> None:
    adapter = FakeW3CAdapter()

    documents = await adapter.fetch()

    assert len(documents) == 1

    document = documents[0]

    assert document.source_identifier == "w3c-wai-news"
    assert document.external_identifier == "w3c-example-001"
    assert document.title == "W3C publishes accessibility guidance"
    assert document.language == "en"
    assert document.metadata["adapter"] == "fake_w3c"
