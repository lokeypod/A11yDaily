import pytest

from app.config.source_config import SourceConfig
from app.config.source_registry import SourceRegistry
from app.ingestion.adapters.static_w3c import StaticW3CAdapter
from app.ingestion.configured_ingestion_service import (
    ConfiguredIngestionService,
)
from app.ingestion.html_normalizer import HtmlDocumentNormalizer
from app.ingestion.ingestion_service import IngestionService


class RecordingIngestionService(IngestionService):
    def __init__(self) -> None:
        self.ingested_source_ids: list[str] = []

    async def ingest(self, adapter, normalizer):
        assert isinstance(normalizer, HtmlDocumentNormalizer)

        documents = await adapter.fetch()

        self.ingested_source_ids.extend(
            document.source_identifier for document in documents
        )

        return documents


@pytest.mark.asyncio
async def test_ingest_all_processes_only_enabled_sources(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    registry = SourceRegistry(
        sources=[
            SourceConfig(
                id="w3c-wai",
                name="W3C WAI",
                type="rss",
                url="https://example.com/w3c.xml",
                enabled=True,
            ),
            SourceConfig(
                id="disabled-source",
                name="Disabled Source",
                type="rss",
                url="https://example.com/disabled.xml",
                enabled=False,
            ),
        ]
    )

    monkeypatch.setattr(
        "app.ingestion.configured_ingestion_service.AdapterFactory.create",
        lambda source: StaticW3CAdapter(),
    )

    ingestion_service = RecordingIngestionService()
    service = ConfiguredIngestionService(
        registry=registry,
        ingestion_service=ingestion_service,
    )

    await service.ingest_all()

    assert ingestion_service.ingested_source_ids == ["w3c-wai-news"]
