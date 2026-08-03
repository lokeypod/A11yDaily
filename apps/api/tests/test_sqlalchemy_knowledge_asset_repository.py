from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from app.domain.knowledge_asset import KnowledgeAsset
from app.persistence.repositories.sqlalchemy_knowledge_asset_repository import (
    SqlAlchemyKnowledgeAssetRepository,
)


def create_asset(
    *,
    title: str = "Example Title",
    summary: str = "Example Summary",
    published_day: int = 20,
) -> KnowledgeAsset:
    asset_id = uuid4()

    return KnowledgeAsset(
        id=asset_id,
        title=title,
        url=f"https://example.com/assets/{asset_id}",
        summary=summary,
        ai_summary=None,
        content_hash=asset_id.hex.ljust(64, "0"),
        published_at=datetime(2026, 7, published_day, tzinfo=UTC),
        discovered_at=datetime(2026, 7, 21, tzinfo=UTC),
    )


def test_find_recent_searches_title_case_insensitively(
    database_session: Session,
) -> None:
    repository = SqlAlchemyKnowledgeAssetRepository(database_session)

    repository.save(
        create_asset(
            title="WCAG 2.2 Focus Appearance",
            summary="Latest WCAG guidance",
            published_day=20,
        )
    )

    repository.save(
        create_asset(
            title="European Accessibility Act",
            summary="Legislation overview",
            published_day=19,
        )
    )

    results = repository.find_recent(query="focus")

    assert len(results) == 1
    assert results[0].title == "WCAG 2.2 Focus Appearance"


def test_find_recent_searches_summary(
    database_session: Session,
) -> None:
    repository = SqlAlchemyKnowledgeAssetRepository(database_session)

    repository.save(
        create_asset(
            title="Document accessibility update",
            summary="New guidance for creating accessible PDF files",
        )
    )

    repository.save(
        create_asset(
            title="Keyboard testing techniques",
            summary="Testing interactive controls without a mouse",
        )
    )

    results = repository.find_recent(query="PDF")

    assert len(results) == 1
    assert results[0].title == "Document accessibility update"


def test_find_recent_trims_whitespace_from_query(
    database_session: Session,
) -> None:
    repository = SqlAlchemyKnowledgeAssetRepository(database_session)

    repository.save(
        create_asset(
            title="PDF Accessibility Techniques",
            summary="Creating tagged PDF documents",
        )
    )

    results = repository.find_recent(query="   pdf   ")

    assert len(results) == 1
    assert results[0].title == "PDF Accessibility Techniques"


def test_find_recent_returns_empty_list_when_query_has_no_matches(
    database_session: Session,
) -> None:
    repository = SqlAlchemyKnowledgeAssetRepository(database_session)

    repository.save(
        create_asset(
            title="WCAG 2.2 Focus Appearance",
            summary="Latest WCAG guidance",
        )
    )

    results = repository.find_recent(query="bananas")

    assert results == []
