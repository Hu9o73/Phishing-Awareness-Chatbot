
from app.database.interactors.Admin.organization import AdminOrganizationInteractor
from app.models.base_models import OrganizationCreationModel, OrganizationModel
from fastapi import APIRouter
from fastapi.security import HTTPBearer

router = APIRouter()
security = HTTPBearer()

@router.post("/organization", response_model=OrganizationModel)
async def create_org(
    organization_name: str,
    organization_description: str | None,
):
    organization = OrganizationCreationModel(name=organization_name, description=organization_description)
    return await AdminOrganizationInteractor.create_organization(organization)
