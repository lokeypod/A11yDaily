from app.ingestion.source_adapter import SourceAdapter


def test_source_adapter_is_abstract() -> None:
    assert SourceAdapter.__abstractmethods__ == {"fetch"}
