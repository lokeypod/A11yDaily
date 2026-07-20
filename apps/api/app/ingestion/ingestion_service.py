from app.ingestion.normalized_document import NormalizedDocument
from app.ingestion.normalizer import DocumentNormalizer
from app.ingestion.source_adapter import SourceAdapter


class IngestionService:
    """Coordinates retrieval and normalization of source content."""

    async def ingest(
        self,
        adapter: SourceAdapter,
        normalizer: DocumentNormalizer,
    ) -> list[NormalizedDocument]:
        raw_documents = await adapter.fetch()

        return [normalizer.normalize(document) for document in raw_documents]
