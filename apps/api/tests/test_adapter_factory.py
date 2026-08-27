from uuid import uuid4

import pytest

from app.domain.source import ConnectorType, Source, SourceType
from app.ingestion.adapter_factory import AdapterFactory
from app.ingestion.adapters.rss import RSSSourceAdapter


def test_factory_creates_rss_adapter() -> None:
    source = Source(
        id=uuid4(),
        organization_id=uuid4(),
        name="W3C Web Accessibility Initiative",
        url="https://www.w3.org/WAI/feed.xml",
        source_type=SourceType.STANDARDS,
        connector_type=ConnectorType.RSS,
        authority_score=100,
        active=True,
        refresh_minutes=60,
        description=None,
    )

    adapter = AdapterFactory.create(source)

    assert isinstance(adapter, RSSSourceAdapter)


def test_factory_rejects_unsupported_connector_type() -> None:
    source = Source(
        id=uuid4(),
        organization_id=uuid4(),
        name="Unsupported Source",
        url="https://example.com",
        source_type=SourceType.COMMUNITY,
        connector_type=ConnectorType.MANUAL,
        authority_score=50,
        active=True,
        refresh_minutes=60,
        description=None,
    )

    with pytest.raises(
        ValueError,
        match="Unsupported connector type: manual",
    ):
        AdapterFactory.create(source)
