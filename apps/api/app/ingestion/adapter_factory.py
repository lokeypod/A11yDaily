from app.config.source_config import SourceConfig
from app.ingestion.adapters.rss import RSSSourceAdapter
from app.ingestion.source_adapter import SourceAdapter


class AdapterFactory:
    """Create source adapters from source configuration."""

    @staticmethod
    def create(source: SourceConfig) -> SourceAdapter:
        if source.type == "rss":
            return RSSSourceAdapter(
                source_identifier=source.id,
                feed_url=source.url,
            )

        raise ValueError(f"Unsupported source type: {source.type}")
