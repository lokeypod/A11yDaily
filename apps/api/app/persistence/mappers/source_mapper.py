from app.domain.source import Source, SourceHealthStatus
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
            health_status=source.health_status.value,
            last_attempt_at=source.last_attempt_at,
            last_success_at=source.last_success_at,
            consecutive_failures=source.consecutive_failures,
            last_error=source.last_error,
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
            health_status=SourceHealthStatus(model.health_status),
            last_attempt_at=model.last_attempt_at,
            last_success_at=model.last_success_at,
            consecutive_failures=model.consecutive_failures,
            last_error=model.last_error,
            refresh_minutes=model.refresh_minutes,
            description=model.description,
        )
