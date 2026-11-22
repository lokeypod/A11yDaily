from app.domain.source import ConnectorType, Source
from app.ingestion.adapters.html_listing import HTMLListingSourceAdapter
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
        if source.connector_type is ConnectorType.SCRAPER:
            if (
                source.scraper_item_selector is None
                or source.scraper_title_selector is None
                or source.scraper_link_selector is None
            ):
                
                raise ValueError(
                    "Scraper source is missing selector "
                    f"configuration: {source.name}"
                )
        
            return HTMLListingSourceAdapter(
                source_identifier=str(source.id),
                listing_url=source.url,
                item_selector=source.scraper_item_selector,
                title_selector=source.scraper_title_selector,
                link_selector=source.scraper_link_selector,
            )

        raise ValueError(f"Unsupported connector type: {source.connector_type.value}")
        