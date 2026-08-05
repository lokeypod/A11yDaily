from uuid import uuid4

from sqlalchemy.orm import Session

from app.domain.organization import Organization
from app.persistence.repositories.sqlalchemy_organization_repository import (
    SqlAlchemyOrganizationRepository,
)


def create_organization(
    *,
    name: str = "W3C",
    website: str = "https://www.w3.org",
) -> Organization:
    return Organization(
        id=uuid4(),
        name=name,
        website=website,
        description="Accessibility organization",
        authority_score=100,
        verified=True,
    )


def test_save_and_get_by_name(
    database_session: Session,
) -> None:
    repository = SqlAlchemyOrganizationRepository(database_session)

    organization = create_organization()

    repository.save(organization)

    result = repository.get_by_name("W3C")

    assert result == organization


def test_get_by_id(
    database_session: Session,
) -> None:
    repository = SqlAlchemyOrganizationRepository(database_session)

    organization = create_organization()

    repository.save(organization)

    result = repository.get_by_id(organization.id)

    assert result == organization


def test_get_by_name_returns_none_when_missing(
    database_session: Session,
) -> None:
    repository = SqlAlchemyOrganizationRepository(database_session)

    result = repository.get_by_name("Adobe")

    assert result is None


def test_get_all_returns_organizations_alphabetically(
    database_session: Session,
) -> None:
    repository = SqlAlchemyOrganizationRepository(database_session)

    repository.save(
        create_organization(
            name="W3C",
            website="https://www.w3.org",
        )
    )
    repository.save(
        create_organization(
            name="Adobe",
            website="https://www.adobe.com",
        )
    )
    repository.save(
        create_organization(
            name="Deque",
            website="https://www.deque.com",
        )
    )

    results = repository.get_all()

    assert [organization.name for organization in results] == [
        "Adobe",
        "Deque",
        "W3C",
    ]
