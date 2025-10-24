from uuid import UUID

from app.database.interactors.Admin.organization import AdminOrganizationInteractor
from app.models.base_models import OrganizationCreationModel, OrganizationModel, StatusResponse
from fastapi import HTTPException, status


class AdminOrganizationService:
    @staticmethod
    async def create_organization(organization: OrganizationCreationModel) -> OrganizationModel:
        return await AdminOrganizationInteractor.create_organization(organization)

    @staticmethod
    async def list_organizations(org_id: UUID | None = None) -> list[OrganizationModel]:
        return await AdminOrganizationInteractor.list_organizations(org_id=org_id)

    @staticmethod
    async def delete_organization(org_id: UUID) -> StatusResponse:
        existence_check = await AdminOrganizationInteractor.list_organizations(org_id=org_id)
        if len(existence_check) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")

        return await AdminOrganizationInteractor.delete_organization(org_id=org_id)
