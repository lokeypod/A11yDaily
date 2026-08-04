from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.organization import Organization
from app.persistence.mappers.organization_mapper import (
    OrganizationMapper,
)
from app.persistence.models.organization import OrganizationModel
from app.repositories.organization_repository import (
    OrganizationRepository,
)


class SqlAlchemyOrganizationRepository(
    OrganizationRepository,
):
    """Persist organizations using SQLAlchemy."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_id(
        self,
        organization_id: UUID,
    ) -> Organization | None:
        statement = select(OrganizationModel).where(
            OrganizationModel.id == organization_id
        )

        model = self._session.scalar(statement)

        if model is None:
            return None

        return OrganizationMapper.to_domain(model)

    def get_by_name(
        self,
        name: str,
    ) -> Organization | None:
        statement = select(OrganizationModel).where(OrganizationModel.name == name)

        model = self._session.scalar(statement)

        if model is None:
            return None

        return OrganizationMapper.to_domain(model)

    def get_all(
        self,
    ) -> list[Organization]:
        statement = select(OrganizationModel).order_by(OrganizationModel.name)

        models = self._session.scalars(statement).all()

        return [OrganizationMapper.to_domain(model) for model in models]

    def save(
        self,
        organization: Organization,
    ) -> Organization:
        model = OrganizationMapper.to_model(organization)

        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)

        return OrganizationMapper.to_domain(model)
