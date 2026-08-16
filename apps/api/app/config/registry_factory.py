from uuid import uuid4

from app.domain.organization import Organization
from app.domain.source import ConnectorType, Source, SourceType


def create_organizations(
    entries: list[dict],
) -> tuple[list[Organization], dict[str, Organization]]:
    organizations: list[Organization] = []
    organizations_by_slug: dict[str, Organization] = {}

    for entry in entries:
        organization = Organization(
            id=uuid4(),
            name=entry["name"],
            website=entry["website"],
            description=entry.get("description"),
            authority_score=entry.get("authority_score", 100),
            verified=entry.get("verified", True),
        )

        organizations.append(organization)
        organizations_by_slug[entry["slug"]] = organization

    return organizations, organizations_by_slug


def create_sources(
    entries: list[dict],
    organizations_by_slug: dict[str, Organization],
) -> list[Source]:
    sources: list[Source] = []

    for entry in entries:
        organization = organizations_by_slug[entry["organization"]]

        source = Source(
            id=uuid4(),
            organization_id=organization.id,
            name=entry["name"],
            url=entry["url"],
            source_type=SourceType(entry["source_type"]),
            connector_type=ConnectorType(entry["connector_type"]),
            authority_score=entry.get("authority_score", 50),
            active=entry.get("active", True),
            refresh_minutes=entry.get("refresh_minutes", 60),
            description=entry.get("description"),
        )

        sources.append(source)

    return sources
