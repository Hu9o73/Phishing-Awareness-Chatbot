from typing import Optional
from uuid import UUID

from app.database.interactors.Admin.organization import AdminOrganizationInteractor
from app.models.base_models import OrganizationCreationModel, OrganizationModel, StatusResponse
from fastapi import APIRouter
from fastapi.security import HTTPBearer

router = APIRouter()
security = HTTPBearer()

@router.post("/organization", response_model=OrganizationModel)
async def create_org(
    organization_name: str,
    organization_description: Optional[str] = None,
):
    organization = OrganizationCreationModel(name=organization_name, description=organization_description)
    return await AdminOrganizationInteractor.create_organization(organization)


@router.get("/organizations", response_model=list[OrganizationModel])
async def list_organizations():
    return await AdminOrganizationInteractor.list_all_organizations()


@router.delete("/organization", response_model=StatusResponse)
async def delete_organization(organization_id: UUID):
    return await AdminOrganizationInteractor.delete_organization(organization_id)
