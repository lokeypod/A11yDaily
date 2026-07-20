from abc import ABC, abstractmethod

from app.ingestion.normalized_document import NormalizedDocument


class PipelineStage(ABC):
    """One transformation step in the ingestion pipeline."""

    @abstractmethod
    def process(self, document: NormalizedDocument) -> NormalizedDocument:
        """Transform and return a normalized document."""
        raise NotImplementedError
