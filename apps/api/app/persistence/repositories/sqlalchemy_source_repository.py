from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.source import Source
from app.persistence.mappers.source_mapper import SourceMapper
from app.persistence.models.source import SourceModel
from app.repositories.source_repository import SourceRepository


class SqlAlchemySourceRepository(SourceRepository):
    """Persist sources using SQLAlchemy."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_id(
        self,
        source_id: UUID,
    ) -> Source | None:
        statement = select(SourceModel).where(SourceModel.id == source_id)

        model = self._session.scalar(statement)

        if model is None:
            return None

        return SourceMapper.to_domain(model)

    def get_by_name(
        self,
        name: str,
    ) -> Source | None:
        statement = select(SourceModel).where(SourceModel.name == name)

        model = self._session.scalar(statement)

        if model is None:
            return None

        return SourceMapper.to_domain(model)

    def get_by_organization_id(
        self,
        organization_id: UUID,
    ) -> list[Source]:
        statement = (
            select(SourceModel)
            .where(SourceModel.organization_id == organization_id)
            .order_by(SourceModel.name)
        )

        models = self._session.scalars(statement).all()

        return [SourceMapper.to_domain(model) for model in models]

    def get_by_organization_id_and_name(
        self,
        organization_id: UUID,
        name: str,
    ) -> Source | None:
        statement = select(SourceModel).where(
            SourceModel.organization_id == organization_id,
            SourceModel.name == name,
        )

        model = self._session.scalar(statement)

        if model is None:
            return None

        return SourceMapper.to_domain(model)

    def get_all(
        self,
    ) -> list[Source]:
        statement = select(SourceModel).order_by(SourceModel.name)

        models = self._session.scalars(statement).all()

        return [SourceMapper.to_domain(model) for model in models]

    def save(
        self,
        source: Source,
    ) -> Source:
        model = SourceMapper.to_model(source)

        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)

        return SourceMapper.to_domain(model)

    def get_by_url(
        self,
        url: str,
    ) -> Source | None:
        statement = select(SourceModel).where(SourceModel.url == url)

        model = self._session.scalar(statement)

        if model is None:
            return None

        return SourceMapper.to_domain(model)

    def update(
        self,
        source: Source,
    ) -> Source:
        model = self._session.get(SourceModel, source.id)

        if model is None:
            raise ValueError(f"Source not found: {source.id}")

        model.organization_id = source.organization_id
        model.name = source.name
        model.url = source.url
        model.source_type = source.source_type
        model.connector_type = source.connector_type
        model.authority_score = source.authority_score
        model.active = source.active
        model.refresh_minutes = source.refresh_minutes
        model.description = source.description

        self._session.commit()
        self._session.refresh(model)

        return SourceMapper.to_domain(model)
