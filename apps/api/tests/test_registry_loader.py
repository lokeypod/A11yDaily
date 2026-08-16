from app.config.registry_loader import (
    load_organizations,
    load_sources,
)


def test_load_organizations() -> None:
    organizations = load_organizations()

    assert len(organizations) > 0

    w3c = next(
        organization for organization in organizations if organization["slug"] == "w3c"
    )

    assert w3c["name"] == "W3C"
    assert w3c["authority_score"] == 100
    assert w3c["verified"] is True


def test_load_sources() -> None:
    sources = load_sources()

    assert len(sources) > 0

    wai_news = next(source for source in sources if source["name"] == "WAI News")

    assert wai_news["organization"] == "w3c"
    assert wai_news["connector_type"] == "rss"
    assert wai_news["source_type"] == "standards"
    assert wai_news["active"] is True
