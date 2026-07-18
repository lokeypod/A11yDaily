from abc import ABC, abstractmethod

from .raw_document import RawDocument


class SourceAdapter(ABC):
    """Base class for every A11yDaily source."""

    @abstractmethod
    async def fetch(self) -> list[RawDocument]:
        """Retrieve new content from a source."""
        raise NotImplementedError
