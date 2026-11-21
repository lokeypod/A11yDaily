
from datetime import UTC, datetime
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

from app.ingestion.raw_document import RawDocument
from app.ingestion.source_adapter import SourceAdapter


class HTMLListingSourceAdapter(SourceAdapter):
    """Retrieve resource links from an HTML listing page."""

    def __init__(
        self,
        source_identifier: str,
        listing_url: str,
        item_selector: str,
        title_selector: str,
        link_selector: str,
        timeout_seconds: float = 20.0,
    ) -> None:
        self._source_identifier = source_identifier
        self._listing_url = listing_url
        self._item_selector = item_selector
        self._title_selector = title_selector
        self._link_selector = link_selector
        self._timeout_seconds = timeout_seconds

    async def fetch(self) -> list[RawDocument]:
        async with httpx.AsyncClient(
            timeout=self._timeout_seconds,
            follow_redirects=True,
        ) as client:
            response = await client.get(self._listing_url)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        retrieved_at = datetime.now(UTC)

        documents: list[RawDocument] = []
        seen_urls: set[str] = set()

        listing_host = urlparse(self._listing_url).netloc

        for item in soup.select(self._item_selector):
            title_element = item.select_one(self._title_selector)
            link = item.select_one(self._link_selector)

            if title_element is None or link is None:
                continue

            href = link.get("href")

            if not isinstance(href, str) or not href.strip():
                continue

            title = title_element.get_text(" ", strip=True)
            url = urljoin(self._listing_url, href)

            parsed_url = urlparse(url)

            if parsed_url.scheme not in {"http", "https"}:
                continue

            if parsed_url.netloc != listing_host:
                continue

            if not title or url in seen_urls:
                continue

            seen_urls.add(url)

            documents.append(
                RawDocument(
                    source_identifier=self._source_identifier,
                    external_identifier=url,
                    title=title,
                    url=url,
                    retrieved_at=retrieved_at,
                    published_at=None,
                    raw_content=title,
                    source_summary=None,
                    author=None,
                    language=None,
                    metadata={
                        "adapter": "html_listing",
                        "listing_url": self._listing_url,
                    },
                )
            )

        return documents
