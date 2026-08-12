from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from app.domain.organization import Organization
from app.domain.source import ConnectorType, Source, SourceType
from app.persistence.repositories.sqlalchemy_organization_repository import (
    SqlAlchemyOrganizationRepository,
)
from app.persistence.repositories.sqlalchemy_source_repository import (
    SqlAlchemySourceRepository,
)


def create_organization() -> Organization:
    return Organization(
        id=uuid4(),
        name="W3C",
        website="https://www.w3.org",
        description="World Wide Web Consortium",
        authority_score=100,
        verified=True,
    )


def create_source(
    *,
    organization_id: UUID,
    name: str = "W3C Accessibility News",
    url: str = "https://www.w3.org/WAI/news/",
) -> Source:
    return Source(
        id=uuid4(),
        organization_id=organization_id,
        name=name,
        url=url,
        source_type=SourceType.STANDARDS,
        connector_type=ConnectorType.RSS,
        authority_score=100,
        active=True,
        refresh_minutes=60,
        description="Accessibility standards and guidance from W3C.",
    )


def test_save_and_get_by_name(
    database_session: Session,
) -> None:
    organization_repository = SqlAlchemyOrganizationRepository(database_session)
    source_repository = SqlAlchemySourceRepository(database_session)

    organization = create_organization()
    organization_repository.save(organization)

    source = create_source(organization_id=organization.id)
    source_repository.save(source)

    result = source_repository.get_by_name("W3C Accessibility News")

    assert result == source


def test_get_by_id(
    database_session: Session,
) -> None:
    organization_repository = SqlAlchemyOrganizationRepository(database_session)
    source_repository = SqlAlchemySourceRepository(database_session)

    organization = create_organization()
    organization_repository.save(organization)

    source = create_source(
        organization_id=organization.id,
    )

    source_repository.save(source)

    result = source_repository.get_by_id(
        source.id,
    )

    assert result == source


def test_get_by_name_returns_none_when_missing(
    database_session: Session,
) -> None:
    repository = SqlAlchemySourceRepository(database_session)

    result = repository.get_by_name("Not A Real Source")

    assert result is None


def test_get_by_organization_id_returns_only_matching_sources(
    database_session: Session,
) -> None:
    organization_repository = SqlAlchemyOrganizationRepository(database_session)
    source_repository = SqlAlchemySourceRepository(database_session)

    organization_a = create_organization()
    organization_repository.save(organization_a)

    organization_b = Organization(
        id=uuid4(),
        name="Deque",
        website="https://www.deque.com",
        description="Accessibility company",
        authority_score=90,
        verified=True,
    )
    organization_repository.save(organization_b)

    source_repository.save(
        create_source(
            organization_id=organization_a.id,
            name="W3C News",
            url="https://www.w3.org/WAI/news/",
        )
    )

    source_repository.save(
        create_source(
            organization_id=organization_a.id,
            name="W3C Blog",
            url="https://www.w3.org/blog/WAI/",
        )
    )

    source_repository.save(
        create_source(
            organization_id=organization_b.id,
            name="Deque Blog",
            url="https://www.deque.com/blog/",
        )
    )

    results = source_repository.get_by_organization_id(organization_a.id)

    assert len(results) == 2
    assert {source.name for source in results} == {
        "W3C News",
        "W3C Blog",
    }


def test_get_all_returns_sources_alphabetically(
    database_session: Session,
) -> None:
    organization_repository = SqlAlchemyOrganizationRepository(database_session)
    source_repository = SqlAlchemySourceRepository(database_session)

    organization = create_organization()
    organization_repository.save(organization)

    source_repository.save(
        create_source(
            organization_id=organization.id,
            name="W3C News",
            url="https://www.w3.org/WAI/news/",
        )
    )

    source_repository.save(
        create_source(
            organization_id=organization.id,
            name="Adobe Accessibility",
            url="https://www.adobe.com/accessibility/",
        )
    )

    source_repository.save(
        create_source(
            organization_id=organization.id,
            name="Deque Blog",
            url="https://www.deque.com/blog/",
        )
    )

    results = source_repository.get_all()

    assert [source.name for source in results] == [
        "Adobe Accessibility",
        "Deque Blog",
        "W3C News",
    ]
