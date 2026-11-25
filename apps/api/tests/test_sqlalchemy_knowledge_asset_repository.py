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
    published_day: int | None = 20,
    discovered_day: int = 21,
) -> KnowledgeAsset:
    asset_id = uuid4()

    return KnowledgeAsset(
        id=asset_id,
        title=title,
        url=f"https://example.com/assets/{asset_id}",
        summary=summary,
        ai_summary=None,
        content_hash=asset_id.hex.ljust(64, "0"),
        published_at=(
            datetime(2026, 7, published_day, tzinfo=UTC)
            if published_day is not None
            else None
        ),
        discovered_at=datetime(
            2026, 7, discovered_day, tzinfo=UTC
        ),
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


def test_count_applies_search_query(
    database_session: Session,
) -> None:
    repository = SqlAlchemyKnowledgeAssetRepository(database_session)

    repository.save(
        create_asset(
            title="PDF Accessibility Techniques",
            summary="Creating tagged PDF documents",
        )
    )

    repository.save(
        create_asset(
            title="WCAG 2.2 Focus Appearance",
            summary="Latest WCAG guidance",
        )
    )

    repository.save(
        create_asset(
            title="European Accessibility Act",
            summary="Legislation overview",
        )
    )

    total = repository.count(query="pdf")

    assert total == 1


def test_find_recent_returns_newest_assets_first(
    database_session: Session,
) -> None:
    repository = SqlAlchemyKnowledgeAssetRepository(database_session)

    repository.save(
        create_asset(
            title="Old Article",
            published_day=18,
        )
    )

    repository.save(
        create_asset(
            title="Newest Article",
            published_day=20,
        )
    )

    repository.save(
        create_asset(
            title="Middle Article",
            published_day=19,
        )
    )

    results = repository.find_recent()

    assert [asset.title for asset in results] == [
        "Newest Article",
        "Middle Article",
        "Old Article",
    ]


def test_find_recent_applies_offset_and_limit(
    database_session: Session,
) -> None:
    repository = SqlAlchemyKnowledgeAssetRepository(database_session)

    repository.save(
        create_asset(
            title="Newest Article",
            published_day=20,
        )
    )

    repository.save(
        create_asset(
            title="Middle Article",
            published_day=19,
        )
    )

    repository.save(
        create_asset(
            title="Oldest Article",
            published_day=18,
        )
    )

    results = repository.find_recent(
        offset=1,
        limit=1,
    )

    assert len(results) == 1
    assert results[0].title == "Middle Article"

def test_find_recent_uses_discovery_date_when_publication_is_unknown(
    database_session: Session,
) -> None:
    repository = SqlAlchemyKnowledgeAssetRepository(database_session)

    repository.save(
        create_asset(
            title="Older Published Article",
            published_day=18,
            discovered_day=25,
        )
    )

    repository.save(
        create_asset(
            title="Undated Resource",
            published_day=None,
            discovered_day=21,
        )
    )

    repository.save(
        create_asset(
            title="Newest Published Article",
            published_day=23,
            discovered_day=24,
        )
    )

    results = repository.find_recent()

    assert [asset.title for asset in results] == [
        "Newest Published Article",
        "Undated Resource",
        "Older Published Article",
    ]

def test_repository_preserves_unknown_publication_date(
    database_session: Session,
) -> None:
    repository = SqlAlchemyKnowledgeAssetRepository(database_session)

    asset = create_asset(
        title="Undated Accessibility Resource",
        published_day=None,
        discovered_day=22,
    )

    saved_asset = repository.save(asset)

    assert saved_asset.published_at is None

    results = repository.find_recent()

    assert len(results) == 1
    assert results[0].id == asset.id
    assert results[0].published_at is None
    assert results[0].discovered_at.date() == asset.discovered_at.date()