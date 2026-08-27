from uuid import uuid4

import pytest

from app.domain.knowledge_asset import KnowledgeAsset
from app.domain.source import ConnectorType, Source, SourceType
from app.ingestion.adapters.static_w3c import StaticW3CAdapter
from app.ingestion.configured_ingestion_service import (
    ConfiguredIngestionService,
)
from app.ingestion.html_normalizer import HtmlDocumentNormalizer
from app.ingestion.ingestion_service import IngestionService
from app.ingestion.normalized_document import NormalizedDocument


class FakeSourceRepository:
    """Test double that returns configured source domain objects."""

    def __init__(self, sources: list[Source]) -> None:
        self._sources = sources

    def get_all(self) -> list[Source]:
        return self._sources


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


def create_source(
    *,
    name: str,
    active: bool,
) -> Source:
    return Source(
        id=uuid4(),
        organization_id=uuid4(),
        name=name,
        url=f"https://example.com/{name.lower().replace(' ', '-')}.xml",
        source_type=SourceType.STANDARDS,
        connector_type=ConnectorType.RSS,
        authority_score=100,
        active=active,
        refresh_minutes=60,
        description=None,
    )


@pytest.mark.asyncio
async def test_ingest_all_processes_only_active_sources(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source_repository = FakeSourceRepository(
        sources=[
            create_source(
                name="W3C WAI",
                active=True,
            ),
            create_source(
                name="Disabled Source",
                active=False,
            ),
        ]
    )

    def create_static_adapter(
        source: Source,
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
        source_repository=source_repository,
        ingestion_service=ingestion_service,
        persistence_service=persistence_service,
    )

    await service.ingest_all()

    assert ingestion_service.ingested_source_ids == ["w3c-wai-news"]
    assert len(persistence_service.persisted_documents) == 1
    assert (
        persistence_service.persisted_documents[0].source_identifier == "w3c-wai-news"
    )
