from uuid import UUID

from app.database.interactors.OrgAdmin.organization import OrgAdminOrganizationInteractor
from app.models.base_models import OrgMemberCreationModel, OrgMemberModel, StatusResponse
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

router = APIRouter()
security = HTTPBearer()

@router.get("/member", response_model=OrgMemberModel)
async def get_member_by_id(member_id: UUID):
    return await OrgAdminOrganizationInteractor.get_member_by_id(member_id)

@router.get("/members", response_model=list[OrgMemberModel])
async def get_members_in_organization(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    return await OrgAdminOrganizationInteractor.get_members_in_organization(token)

@router.post("/member", response_model=OrgMemberModel)
async def create_member(member: OrgMemberCreationModel):
    return await OrgAdminOrganizationInteractor.create_member(member)

@router.delete("/member", response_model=StatusResponse)
async def delete_member(member_id: UUID):
    return await OrgAdminOrganizationInteractor.delete_member(member_id)
