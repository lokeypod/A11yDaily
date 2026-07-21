import pytest

from app.config.source_config import SourceConfig
from app.ingestion.adapter_factory import AdapterFactory
from app.ingestion.adapters.rss import RSSSourceAdapter


def test_factory_creates_rss_adapter() -> None:
    source = SourceConfig(
        id="w3c-wai",
        name="W3C Web Accessibility Initiative",
        type="rss",
        url="https://www.w3.org/WAI/feed.xml",
        enabled=True,
    )

    adapter = AdapterFactory.create(source)

    assert isinstance(adapter, RSSSourceAdapter)


def test_factory_rejects_unknown_source_type() -> None:
    source = SourceConfig(
        id="unknown-source",
        name="Unknown Source",
        type="unsupported",
        url="https://example.com",
        enabled=True,
    )

    with pytest.raises(
        ValueError,
        match="Unsupported source type: unsupported",
    ):
        AdapterFactory.create(source)
