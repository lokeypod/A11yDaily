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
