from app.config.registry_factory import (
    create_organizations,
    create_sources,
)
from app.config.registry_loader import (
    load_organizations,
    load_sources,
)
from app.database.session import SessionLocal
from app.domain.organization import Organization
from app.persistence.repositories.sqlalchemy_organization_repository import (
    SqlAlchemyOrganizationRepository,
)
from app.persistence.repositories.sqlalchemy_source_repository import (
    SqlAlchemySourceRepository,
)


def seed() -> None:
    """Seed the database from the accessibility knowledge registry."""

    session = SessionLocal()

    try:
        organization_repository = SqlAlchemyOrganizationRepository(session)
        source_repository = SqlAlchemySourceRepository(session)

        organization_entries = load_organizations()
        source_entries = load_sources()

        organizations, organizations_by_slug = create_organizations(
            organization_entries
        )

        persisted_by_slug: dict[str, Organization] = {}

        for entry, organization in zip(
            organization_entries,
            organizations,
            strict=True,
        ):
            existing = organization_repository.get_by_name(organization.name)

            if existing is None:
                persisted = organization_repository.save(organization)
            else:
                persisted = existing

            persisted_by_slug[entry["slug"]] = persisted

        sources = create_sources(
            source_entries,
            persisted_by_slug,
        )

        for source in sources:
            existing = source_repository.get_by_url(source.url)

            if existing is None:
                source_repository.save(source)

    finally:
        session.close()


if __name__ == "__main__":
    seed()
