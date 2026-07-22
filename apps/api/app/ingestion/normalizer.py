from abc import ABC, abstractmethod

from app.ingestion.normalized_document import NormalizedDocument
from app.ingestion.raw_document import RawDocument


class DocumentNormalizer(ABC):
    """Contract for converting raw documents into canonical documents."""

    @abstractmethod
    def normalize(self, document: RawDocument) -> NormalizedDocument:
        """Convert a raw document into A11yDaily's canonical representation."""
        raise NotImplementedError
