import asyncio

from app.ingestion.adapters.rss import RSSSourceAdapter
from app.ingestion.html_normalizer import HtmlDocumentNormalizer
from app.ingestion.ingestion_service import IngestionService
from app.ingestion.pipeline import IngestionPipeline
from app.ingestion.stages.content_hash import ContentHashStage


async def main() -> None:
    adapter = RSSSourceAdapter(
        source_identifier="w3c-wai-news",
        feed_url="https://www.w3.org/WAI/feed.xml",
    )

    pipeline = IngestionPipeline(
        stages=[
            ContentHashStage(),
        ]
    )

    service = IngestionService(pipeline=pipeline)

    documents = await service.ingest(
        adapter=adapter,
        normalizer=HtmlDocumentNormalizer(),
    )

    print(f"Retrieved {len(documents)} W3C WAI documents.")

    for document in documents:
        print()
        print(f"Title: {document.title}")
        print(f"URL: {document.canonical_url}")
        print(f"Published: {document.published_at}")
        print(f"Hash: {document.content_hash}")
        print(f"Preview: {document.plain_text[:160]}")


if __name__ == "__main__":
    asyncio.run(main())
