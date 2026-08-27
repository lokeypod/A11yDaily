from uuid import uuid4

from app.database import seed as seed_module
from app.domain.organization import Organization
from app.domain.source import ConnectorType, Source, SourceType


class FakeOrganizationRepository:
    def __init__(self) -> None:
        self._organizations: list[Organization] = []

    def get_by_name(self, name: str) -> Organization | None:
        return next(
            (
                organization
                for organization in self._organizations
                if organization.name == name
            ),
            None,
        )

    def save(self, organization: Organization) -> Organization:
        self._organizations.append(organization)
        return organization


class FakeSourceRepository:
    existing_source: Source | None = None
    updated_source: Source | None = None

    def get_by_organization_id_and_name(
        self,
        organization_id,
        name,
    ) -> Source | None:
        source = type(self).existing_source

        if source is None:
            return None

        if source.organization_id == organization_id and source.name == name:
            return source

        return None

    def save(self, source: Source) -> Source:
        type(self).existing_source = source
        return source

    def update(self, source: Source) -> Source:
        type(self).updated_source = source
        type(self).existing_source = source
        return source

    def get_all(self) -> list[Source]:
        source = type(self).existing_source

        if source is None:
            return []

        return [source]


class FakeSession:
    def close(self) -> None:
        pass


def test_seed_updates_existing_source_when_registry_url_changes(
    monkeypatch,
) -> None:
    organization_id = uuid4()

    organization = Organization(
        id=organization_id,
        name="W3C",
        website="https://www.w3.org",
    )

    existing_source = Source(
        id=uuid4(),
        organization_id=organization_id,
        name="WAI News",
        url="https://www.w3.org/WAI/news/",
        source_type=SourceType.STANDARDS,
        connector_type=ConnectorType.RSS,
        active=False,
    )

    FakeSourceRepository.existing_source = existing_source
    FakeSourceRepository.updated_source = None

    def create_fake_organization_repository(session):
        del session
        return FakeOrganizationRepository()

    def create_fake_source_repository(session):
        del session
        return FakeSourceRepository()

    def fake_create_organizations(entries):
        del entries

        return (
            [organization],
            {"w3c": organization},
        )

    def fake_create_sources(
        entries,
        organizations_by_slug,
    ):
        del entries
        del organizations_by_slug

        return [
            Source(
                id=uuid4(),
                organization_id=organization_id,
                name="WAI News",
                url="https://www.w3.org/WAI/feed.xml",
                source_type=SourceType.STANDARDS,
                connector_type=ConnectorType.RSS,
                active=True,
            )
        ]

    monkeypatch.setattr(
        seed_module,
        "SessionLocal",
        lambda: FakeSession(),
    )

    monkeypatch.setattr(
        seed_module,
        "SqlAlchemyOrganizationRepository",
        create_fake_organization_repository,
    )

    monkeypatch.setattr(
        seed_module,
        "SqlAlchemySourceRepository",
        create_fake_source_repository,
    )

    monkeypatch.setattr(
        seed_module,
        "load_organizations",
        lambda: [
            {
                "slug": "w3c",
                "name": "W3C",
                "website": "https://www.w3.org",
            }
        ],
    )

    monkeypatch.setattr(
        seed_module,
        "create_organizations",
        fake_create_organizations,
    )

    monkeypatch.setattr(
        seed_module,
        "load_sources",
        lambda: [
            {
                "organization": "w3c",
                "name": "WAI News",
                "url": "https://www.w3.org/WAI/feed.xml",
                "source_type": "standards",
                "connector_type": "rss",
                "active": True,
            }
        ],
    )

    monkeypatch.setattr(
        seed_module,
        "create_sources",
        fake_create_sources,
    )

    seed_module.seed()

    updated = FakeSourceRepository.updated_source

    assert updated is not None
    assert updated.id == existing_source.id
    assert updated.url == "https://www.w3.org/WAI/feed.xml"
    assert updated.active is True
