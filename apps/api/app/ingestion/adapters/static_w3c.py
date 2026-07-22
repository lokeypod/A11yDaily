from datetime import UTC, datetime

from app.ingestion.raw_document import RawDocument
from app.ingestion.source_adapter import SourceAdapter


class StaticW3CAdapter(SourceAdapter):
    """Static adapter that returns predictable W3C-style content."""

    async def fetch(self) -> list[RawDocument]:
        return [
            RawDocument(
                source_identifier="w3c-wai-news",
                external_identifier="w3c-example-001",
                title="W3C publishes accessibility guidance",
                url="https://www.w3.org/WAI/example",
                retrieved_at=datetime.now(UTC),
                published_at=datetime(2026, 7, 1, tzinfo=UTC),
                raw_content="<p>Example accessibility guidance.</p>",
                source_summary="Example guidance published by the W3C.",
                author="W3C Web Accessibility Initiative",
                language="en",
                metadata={
                    "adapter": "static_w3c",
                    "content_type": "text/html",
                },
            )
        ]
