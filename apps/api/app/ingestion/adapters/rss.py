from datetime import UTC, datetime
from time import struct_time
from typing import Any

import feedparser
import httpx

from app.ingestion.raw_document import RawDocument
from app.ingestion.source_adapter import SourceAdapter


class RSSSourceAdapter(SourceAdapter):
    """Retrieve and parse entries from an RSS or Atom feed."""

    def __init__(
        self,
        source_identifier: str,
        feed_url: str,
        timeout_seconds: float = 20.0,
    ) -> None:
        self._source_identifier = source_identifier
        self._feed_url = feed_url
        self._timeout_seconds = timeout_seconds

    async def fetch(self) -> list[RawDocument]:
        async with httpx.AsyncClient(
            timeout=self._timeout_seconds,
            follow_redirects=True,
        ) as client:
            response = await client.get(self._feed_url)
            response.raise_for_status()

        parsed_feed = feedparser.parse(response.content)
        retrieved_at = datetime.now(UTC)

        return [
            self._to_raw_document(entry, retrieved_at) for entry in parsed_feed.entries
        ]

    def _to_raw_document(
        self,
        entry: dict[str, Any],
        retrieved_at: datetime,
    ) -> RawDocument:
        url = str(entry.get("link", "")).strip()
        external_identifier = str(entry.get("id") or entry.get("guid") or url).strip()

        return RawDocument(
            source_identifier=self._source_identifier,
            external_identifier=external_identifier,
            title=str(entry.get("title", "Untitled")).strip(),
            url=url,
            retrieved_at=retrieved_at,
            published_at=self._parse_datetime(
                entry.get("published_parsed") or entry.get("updated_parsed")
            ),
            raw_content=self._extract_content(entry),
            source_summary=self._optional_string(entry.get("summary")),
            author=self._optional_string(entry.get("author")),
            language=self._optional_string(entry.get("language")),
            metadata={
                "adapter": "rss",
                "feed_url": self._feed_url,
            },
        )

    @staticmethod
    def _extract_content(entry: dict[str, Any]) -> str | None:
        content = entry.get("content")

        if isinstance(content, list) and content:
            value = content[0].get("value")

            if value:
                return str(value)

        summary = entry.get("summary")

        return str(summary) if summary else None

    @staticmethod
    def _parse_datetime(value: struct_time | None) -> datetime | None:
        if value is None:
            return None

        return datetime(
            year=value.tm_year,
            month=value.tm_mon,
            day=value.tm_mday,
            hour=value.tm_hour,
            minute=value.tm_min,
            second=value.tm_sec,
            tzinfo=UTC,
        )

    @staticmethod
    def _optional_string(value: object) -> str | None:
        if value is None:
            return None

        normalized = str(value).strip()
        return normalized or None
