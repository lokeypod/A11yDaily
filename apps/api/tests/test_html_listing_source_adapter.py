
import httpx
import pytest

from app.ingestion.adapters.html_listing import (
    HTMLListingSourceAdapter,
)


@pytest.mark.asyncio
async def test_html_listing_adapter_extracts_unique_same_origin_links(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    html = """
    <html>
        <body>
            <div class="article-card">
                <h2>Article One</h2>
                <a href="/article-one/">Read more</a>
            </div>

            <div class="article-card">
                <h2>Article Two</h2>
                <a href="https://example.com/article-two/">
                    Read more
                </a>
            </div>

            <div class="article-card">
                <h2>Duplicate Article</h2>
                <a href="/article-one/">Read more</a>
            </div>

            <div class="article-card">
                <h2>External Resource</h2>
                <a href="https://external.example.org/resource">
                    Read more
                </a>
            </div>

            <div class="article-card">
                <h2>Missing Link</h2>
            </div>
        </body>
    </html>
    """

    class FakeResponse:
        text = html

        def raise_for_status(self) -> None:
            return None

    class FakeAsyncClient:
        async def __aenter__(self):
            return self

        async def __aexit__(
            self,
            exc_type,
            exc,
            traceback,
        ) -> None:
            return None

        async def get(self, url: str) -> FakeResponse:
            assert url == "https://example.com/news/"
            return FakeResponse()

    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        lambda **kwargs: FakeAsyncClient(),
    )

    adapter = HTMLListingSourceAdapter(
        source_identifier="example-source",
        listing_url="https://example.com/news/",
        item_selector=".article-card",
        title_selector="h2",
        link_selector="a[href]",
    )

    documents = await adapter.fetch()

    assert len(documents) == 2

    assert documents[0].title == "Article One"
    assert documents[0].url == "https://example.com/article-one/"

    assert documents[1].title == "Article Two"
    assert documents[1].url == "https://example.com/article-two/"

    assert all(
        document.source_identifier == "example-source"
        for document in documents
    )
