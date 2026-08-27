from app.domain.source import ConnectorType, Source
from app.ingestion.adapters.rss import RSSSourceAdapter
from app.ingestion.source_adapter import SourceAdapter


class AdapterFactory:
    """Create source adapters from persisted source definitions."""

    @staticmethod
    def create(source: Source) -> SourceAdapter:
        if source.connector_type is ConnectorType.RSS:
            return RSSSourceAdapter(
                source_identifier=str(source.id),
                feed_url=source.url,
            )

        raise ValueError(f"Unsupported connector type: {source.connector_type.value}")
