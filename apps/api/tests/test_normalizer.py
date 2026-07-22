from app.ingestion.normalizer import DocumentNormalizer


def test_document_normalizer_is_abstract() -> None:
    assert DocumentNormalizer.__abstractmethods__ == {"normalize"}
