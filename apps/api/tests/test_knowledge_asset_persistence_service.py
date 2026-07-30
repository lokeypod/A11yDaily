from datetime import UTC, datetime

from app.domain.knowledge_asset import KnowledgeAsset
from app.ingestion.knowledge_asset_persistence_service import (
    KnowledgeAssetPersistenceService,
)
from app.ingestion.normalized_document import NormalizedDocument
from app.repositories.knowledge_assets_repository import (
    KnowledgeAssetRepository,
)


class InMemoryKnowledgeAssetRepository(KnowledgeAssetRepository):
    def __init__(self) -> None:
        self.assets_by_hash: dict[str, KnowledgeAsset] = {}

    def get_by_content_hash(
        self,
        content_hash: str,
    ) -> KnowledgeAsset | None:
        return self.assets_by_hash.get(content_hash)

    def find_recent(
        self,
        *,
        offset: int = 0,
        limit: int = 20,
    ) -> list[KnowledgeAsset]:
        assets = list(self.assets_by_hash.values())
        return assets[offset : offset + limit]

    def count(self) -> int:
        return len(self.assets_by_hash)

    def save(
        self,
        knowledge_asset: KnowledgeAsset,
    ) -> KnowledgeAsset:
        self.assets_by_hash[knowledge_asset.content_hash] = knowledge_asset
        return knowledge_asset


def find_recent(
    self,
    *,
    offset: int = 0,
    limit: int = 20,
    query: str | None = None,
) -> list[KnowledgeAsset]:
    assets = list(self.assets_by_hash.values())
    return assets[offset : offset + limit]


def count(
    self,
    *,
    query: str | None = None,
) -> int:
    return len(self.assets_by_hash)


def create_document(
    external_identifier: str,
    content_hash: str | None,
) -> NormalizedDocument:
    return NormalizedDocument(
        source_identifier="w3c-wai",
        external_identifier=external_identifier,
        title="Accessibility guidance",
        canonical_url=f"https://example.com/{external_identifier}",
        plain_text="Example accessibility guidance.",
        retrieved_at=datetime(2026, 7, 21, tzinfo=UTC),
        published_at=datetime(2026, 7, 20, tzinfo=UTC),
        source_summary="Publisher summary.",
        content_hash=content_hash,
    )


def test_persistence_service_saves_new_asset() -> None:
    repository = InMemoryKnowledgeAssetRepository()
    service = KnowledgeAssetPersistenceService(repository)

    saved_assets = service.persist([create_document("entry-001", "a" * 64)])

    assert len(saved_assets) == 1
    assert saved_assets[0].content_hash == "a" * 64
    assert len(repository.assets_by_hash) == 1


def test_persistence_service_skips_duplicate_asset() -> None:
    repository = InMemoryKnowledgeAssetRepository()
    service = KnowledgeAssetPersistenceService(repository)
    document = create_document("entry-001", "a" * 64)

    first_result = service.persist([document])
    second_result = service.persist([document])

    assert len(first_result) == 1
    assert second_result == []
    assert len(repository.assets_by_hash) == 1


def test_persistence_service_skips_document_without_hash() -> None:
    repository = InMemoryKnowledgeAssetRepository()
    service = KnowledgeAssetPersistenceService(repository)

    saved_assets = service.persist([create_document("entry-001", None)])

    assert saved_assets == []
    assert repository.assets_by_hash == {}
