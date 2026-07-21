import httpx
import pytest

from app.ingestion.adapters.rss import RSSSourceAdapter

RSS_XML = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>A11yDaily Test Feed</title>
    <link>https://example.com</link>
    <description>Test accessibility feed</description>
    <item>
      <guid>entry-001</guid>
      <title>Accessible documents update</title>
      <link>https://example.com/accessible-documents</link>
      <description>New PDF accessibility guidance.</description>
      <pubDate>Mon, 20 Jul 2026 12:00:00 GMT</pubDate>
    </item>
  </channel>
</rss>
"""


@pytest.mark.asyncio
async def test_rss_adapter_returns_raw_documents(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def fake_get(
        self: httpx.AsyncClient,
        url: str,
    ) -> httpx.Response:
        request = httpx.Request("GET", url)

        return httpx.Response(
            status_code=200,
            content=RSS_XML.encode(),
            request=request,
        )

    monkeypatch.setattr(httpx.AsyncClient, "get", fake_get)

    adapter = RSSSourceAdapter(
        source_identifier="test-accessibility-feed",
        feed_url="https://example.com/feed.xml",
    )

    documents = await adapter.fetch()

    assert len(documents) == 1

    document = documents[0]

    assert document.external_identifier == "entry-001"
    assert document.title == "Accessible documents update"
    assert document.url == "https://example.com/accessible-documents"
    assert document.source_summary == "New PDF accessibility guidance."
    assert document.metadata["adapter"] == "rss"
