from uuid import UUID

from sqlalchemy.orm import Session

from app.domain.organization import Organization
from app.persistence.models.organization import OrganizationModel
from app.repositories.organization_repository import OrganizationRepository


class SqlAlchemyOrganizationRepository(OrganizationRepository):
    """SQLAlchemy implementation of the organization repository."""

    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Organization]:
        models = self.session.query(OrganizationModel).all()
        return [self._to_domain(model) for model in models]

    def get(self, organization_id: UUID) -> Organization | None:
        model = self.session.get(OrganizationModel, organization_id)

        if model is None:
            return None

        return self._to_domain(model)

    def create(self, organization: Organization) -> Organization:
        model = OrganizationModel(
            id=organization.id,
            name=organization.name,
            website=organization.website,
            description=organization.description,
            authority_score=organization.authority_score,
            verified=organization.verified,
        )

        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)

        return self._to_domain(model)

    def _to_domain(self, model: OrganizationModel) -> Organization:
        return Organization(
            id=model.id,
            name=model.name,
            website=model.website,
            description=model.description,
            authority_score=model.authority_score,
            verified=model.verified,
        )