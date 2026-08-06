from app.domain.source import Source
from app.persistence.models.source import SourceModel


class SourceMapper:
    """Convert between source domain and persistence models."""

    @staticmethod
    def to_model(
        source: Source,
    ) -> SourceModel:
        return SourceModel(
            id=source.id,
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

    @staticmethod
    def to_domain(
        model: SourceModel,
    ) -> Source:
        return Source(
            id=model.id,
            organization_id=model.organization_id,
            name=model.name,
            url=model.url,
            source_type=model.source_type,
            connector_type=model.connector_type,
            authority_score=model.authority_score,
            active=model.active,
            refresh_minutes=model.refresh_minutes,
            description=model.description,
        )
