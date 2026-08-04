from app.domain.organization import Organization
from app.persistence.models.organization import OrganizationModel


class OrganizationMapper:
    """Convert between organization domain and persistence models."""

    @staticmethod
    def to_model(
        organization: Organization,
    ) -> OrganizationModel:
        return OrganizationModel(
            id=organization.id,
            name=organization.name,
            website=organization.website,
            description=organization.description,
            authority_score=organization.authority_score,
            verified=organization.verified,
        )

    @staticmethod
    def to_domain(
        model: OrganizationModel,
    ) -> Organization:
        return Organization(
            id=model.id,
            name=model.name,
            website=model.website,
            description=model.description,
            authority_score=model.authority_score,
            verified=model.verified,
        )
