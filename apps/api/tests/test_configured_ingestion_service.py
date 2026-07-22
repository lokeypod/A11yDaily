import pytest

from app.config.source_config import SourceConfig
from app.config.source_registry import SourceRegistry
from app.domain.knowledge_asset import KnowledgeAsset
from app.ingestion.adapters.static_w3c import StaticW3CAdapter
from app.ingestion.configured_ingestion_service import (
    ConfiguredIngestionService,
)
from app.ingestion.html_normalizer import HtmlDocumentNormalizer
from app.ingestion.ingestion_service import IngestionService
from app.ingestion.normalized_document import NormalizedDocument


class RecordingIngestionService(IngestionService):
    """Test double that records which source documents were ingested."""

    def __init__(self) -> None:
        self.ingested_source_ids: list[str] = []

    async def ingest(
        self,
        adapter: StaticW3CAdapter,
        normalizer: HtmlDocumentNormalizer,
    ) -> list[NormalizedDocument]:
        assert isinstance(normalizer, HtmlDocumentNormalizer)

        raw_documents = await adapter.fetch()

        self.ingested_source_ids.extend(
            document.source_identifier for document in raw_documents
        )

        return [normalizer.normalize(document) for document in raw_documents]


class RecordingPersistenceService:
    """Test double that records documents passed to persistence."""

    def __init__(self) -> None:
        self.persisted_documents: list[NormalizedDocument] = []

    def persist(
        self,
        documents: list[NormalizedDocument],
    ) -> list[KnowledgeAsset]:
        self.persisted_documents.extend(documents)
        return []


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

    def create_static_adapter(
        source: SourceConfig,
    ) -> StaticW3CAdapter:
        del source

    return StaticW3CAdapter()

    monkeypatch.setattr(
        "app.ingestion.configured_ingestion_service.AdapterFactory.create",
        create_static_adapter,
    )

    ingestion_service = RecordingIngestionService()
    persistence_service = RecordingPersistenceService()

    service = ConfiguredIngestionService(
        registry=registry,
        ingestion_service=ingestion_service,
        persistence_service=persistence_service,
    )

    await service.ingest_all()

    assert ingestion_service.ingested_source_ids == ["w3c-wai-news"]
    assert len(persistence_service.persisted_documents) == 1
    assert (
        persistence_service.persisted_documents[0].source_identifier == "w3c-wai-news"
    )
