from uuid import uuid4

from app.domain.source import ConnectorType, Source, SourceType
from app.persistence.mappers.source_mapper import SourceMapper


def create_source() -> Source:
    return Source(
        id=uuid4(),
        organization_id=uuid4(),
        name="W3C Accessibility News",
        url="https://www.w3.org/WAI/news/",
        source_type=SourceType.STANDARDS,
        connector_type=ConnectorType.RSS,
        authority_score=100,
        active=True,
        refresh_minutes=60,
        description="Accessibility standards and guidance from W3C.",
    )


def test_mapper_converts_domain_source_to_model() -> None:
    source = create_source()

    model = SourceMapper.to_model(source)

    assert model.id == source.id
    assert model.organization_id == source.organization_id
    assert model.name == source.name
    assert model.url == source.url
    assert model.source_type == source.source_type
    assert model.connector_type == source.connector_type
    assert model.authority_score == source.authority_score
    assert model.active == source.active
    assert model.refresh_minutes == source.refresh_minutes
    assert model.description == source.description


def test_mapper_converts_model_back_to_domain() -> None:
    source = create_source()
    model = SourceMapper.to_model(source)

    result = SourceMapper.to_domain(model)

    assert result == source
