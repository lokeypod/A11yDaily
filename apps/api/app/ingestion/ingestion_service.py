from app.ingestion.normalized_document import NormalizedDocument
from app.ingestion.normalizer import DocumentNormalizer
from app.ingestion.pipeline import IngestionPipeline
from app.ingestion.source_adapter import SourceAdapter


class IngestionService:
    """Coordinates retrieval, normalization, and pipeline processing."""

    def __init__(self, pipeline: IngestionPipeline | None = None) -> None:
        self._pipeline = pipeline or IngestionPipeline()

    async def ingest(
        self,
        adapter: SourceAdapter,
        normalizer: DocumentNormalizer,
    ) -> list[NormalizedDocument]:
        raw_documents = await adapter.fetch()

        normalized_documents = [
            normalizer.normalize(document) for document in raw_documents
        ]

        return self._pipeline.process_all(normalized_documents)
