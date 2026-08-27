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
from app.domain.source import Source
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

        organizations, _ = create_organizations(organization_entries)

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
            existing = source_repository.get_by_organization_id_and_name(
                source.organization_id,
                source.name,
            )

            if existing is None:
                source_repository.save(source)
                continue

            synchronized = Source(
                id=existing.id,
                organization_id=source.organization_id,
                name=source.name,
                url=source.url,
                source_type=source.source_type,
                connector_type=source.connector_type,
                authority_score=source.authority_score,
                active=source.active,
                refresh_minutes=source.refresh_minutes,
                description=source.description,
            )

            source_repository.update(synchronized)

        registry_source_keys = {
            (
                source.organization_id,
                source.name,
            )
            for source in sources
        }

        for persisted_source in source_repository.get_all():
            source_key = (
                persisted_source.organization_id,
                persisted_source.name,
            )

            if source_key in registry_source_keys:
                continue

            if not persisted_source.active:
                continue

            deactivated_source = Source(
                id=persisted_source.id,
                organization_id=persisted_source.organization_id,
                name=persisted_source.name,
                url=persisted_source.url,
                source_type=persisted_source.source_type,
                connector_type=persisted_source.connector_type,
                authority_score=persisted_source.authority_score,
                active=False,
                refresh_minutes=persisted_source.refresh_minutes,
                description=persisted_source.description,
            )

            source_repository.update(deactivated_source)

    finally:
        session.close()


if __name__ == "__main__":
    seed()
