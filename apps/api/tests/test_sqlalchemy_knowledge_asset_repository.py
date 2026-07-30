from datetime import UTC, datetime
from uuid import uuid4

from app.domain.knowledge_asset import KnowledgeAsset
from app.persistence.repositories.sqlalchemy_knowledge_asset_repository import (
    SqlAlchemyKnowledgeAssetRepository,
)


def test_find_recent_searches_title_case_insensitively(
    database_session,
) -> None:
    repository = SqlAlchemyKnowledgeAssetRepository(database_session)

    repository.save(
        KnowledgeAsset(
            id=uuid4(),
            title="WCAG 2.2 Focus Appearance",
            url="https://example.com/wcag22",
            summary="Latest WCAG guidance",
            ai_summary=None,
            content_hash="a" * 64,
            published_at=datetime(2026, 7, 20, tzinfo=UTC),
            discovered_at=datetime(2026, 7, 21, tzinfo=UTC),
        )
    )

    repository.save(
        KnowledgeAsset(
            id=uuid4(),
            title="European Accessibility Act",
            url="https://example.com/eaa",
            summary="Legislation overview",
            ai_summary=None,
            content_hash="b" * 64,
            published_at=datetime(2026, 7, 19, tzinfo=UTC),
            discovered_at=datetime(2026, 7, 21, tzinfo=UTC),
        )
    )

    results = repository.find_recent(query="focus")

    assert len(results) == 1
    assert results[0].title == "WCAG 2.2 Focus Appearance"
