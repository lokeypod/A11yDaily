from app.config.registry_factory import (
    create_organizations,
    create_sources,
)
from app.domain.organization import Organization
from app.domain.source import ConnectorType, Source, SourceType


def test_create_organizations() -> None:
    entries = [
        {
            "slug": "w3c",
            "name": "W3C",
            "website": "https://www.w3.org",
            "description": "World Wide Web Consortium",
            "authority_score": 100,
            "verified": True,
        }
    ]

    organizations, organizations_by_slug = create_organizations(entries)

    assert len(organizations) == 1

    organization = organizations[0]

    assert isinstance(organization, Organization)
    assert organization.name == "W3C"
    assert organization.website == "https://www.w3.org"
    assert organization.authority_score == 100
    assert organizations_by_slug["w3c"] == organization


def test_create_sources_resolves_organization_slug() -> None:
    organization_entries = [
        {
            "slug": "w3c",
            "name": "W3C",
            "website": "https://www.w3.org",
        }
    ]

    organizations, organizations_by_slug = create_organizations(organization_entries)

    source_entries = [
        {
            "organization": "w3c",
            "name": "WAI News",
            "url": "https://www.w3.org/WAI/news/",
            "source_type": "standards",
            "connector_type": "rss",
        }
    ]

    sources = create_sources(
        source_entries,
        organizations_by_slug,
    )

    assert len(sources) == 1

    source = sources[0]

    assert isinstance(source, Source)
    assert source.organization_id == organizations[0].id
    assert source.source_type is SourceType.STANDARDS
    assert source.connector_type is ConnectorType.RSS


def test_registry_factory_applies_defaults() -> None:
    organization_entries = [
        {
            "slug": "w3c",
            "name": "W3C",
            "website": "https://www.w3.org",
        }
    ]

    organizations, organizations_by_slug = create_organizations(organization_entries)

    source_entries = [
        {
            "organization": "w3c",
            "name": "WAI News",
            "url": "https://www.w3.org/WAI/news/",
            "source_type": "standards",
            "connector_type": "rss",
        }
    ]

    sources = create_sources(
        source_entries,
        organizations_by_slug,
    )

    organization = organizations[0]
    source = sources[0]

    assert organization.authority_score == 100
    assert organization.verified is True

    assert source.authority_score == 50
    assert source.active is True
    assert source.refresh_minutes == 60
