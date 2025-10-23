from uuid import UUID

from app.models.base_models import OrgMemberModel, StatusResponse
from app.services.OrgAdmin.organization import OrgAdminOrganizationService
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

router = APIRouter()
security = HTTPBearer()

@router.get("/member", response_model=OrgMemberModel)
async def get_member_by_id(member_id: UUID, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    return await OrgAdminOrganizationService.get_member_by_id(member_id, token)


@router.get("/members", response_model=list[OrgMemberModel])
async def get_members_in_organization(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    return await OrgAdminOrganizationService.get_members_in_organization(token)


@router.post("/member", response_model=OrgMemberModel)
async def create_member(
    email: str, first_name: str, last_name: str, credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    return await OrgAdminOrganizationService.create_member(email, first_name, last_name, token)


@router.delete("/member", response_model=StatusResponse)
async def delete_member(member_id: UUID, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    return await OrgAdminOrganizationService.delete_member(member_id, token)
