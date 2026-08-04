from uuid import uuid4

from app.domain.organization import Organization
from app.persistence.mappers.organization_mapper import (
    OrganizationMapper,
)


def create_organization() -> Organization:
    return Organization(
        id=uuid4(),
        name="W3C",
        website="https://www.w3.org",
        description="World Wide Web Consortium",
        authority_score=100,
        verified=True,
    )


def test_mapper_converts_domain_organization_to_model() -> None:
    organization = create_organization()

    model = OrganizationMapper.to_model(organization)

    assert model.id == organization.id
    assert model.name == organization.name
    assert model.website == organization.website
    assert model.authority_score == organization.authority_score
    assert model.verified == organization.verified


def test_mapper_converts_model_back_to_domain() -> None:
    organization = create_organization()
    model = OrganizationMapper.to_model(organization)

    result = OrganizationMapper.to_domain(model)

    assert result == organization
