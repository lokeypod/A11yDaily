import hashlib

from app.ingestion.normalized_document import NormalizedDocument
from app.ingestion.pipeline_stage import PipelineStage


class ContentHashStage(PipelineStage):
    """Calculate a SHA-256 hash from the document's normalized text."""

    def process(self, document: NormalizedDocument) -> NormalizedDocument:
        document.content_hash = hashlib.sha256(
            document.plain_text.encode("utf-8")
        ).hexdigest()

        return document
