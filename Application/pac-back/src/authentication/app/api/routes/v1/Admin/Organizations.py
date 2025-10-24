from typing import Optional
from uuid import UUID

from app.models.base_models import OrganizationCreationModel, OrganizationModel, StatusResponse
from app.services.Admin.organization import AdminOrganizationService
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
    return await AdminOrganizationService.create_organization(organization)


@router.get("/organizations", response_model=list[OrganizationModel])
async def list_organizations():
    return await AdminOrganizationService.list_organizations()


@router.delete("/organization", response_model=StatusResponse)
async def delete_organization(organization_id: UUID):
    return await AdminOrganizationService.delete_organization(organization_id)
