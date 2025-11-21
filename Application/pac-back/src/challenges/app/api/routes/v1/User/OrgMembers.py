from uuid import UUID

from app.models.base_models import OrgMemberModel
from app.services.User.organization import UserOrganizationService
from fastapi import APIRouter, Depends, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

router = APIRouter()
security = HTTPBearer()


@router.get("/organization/members", response_model=list[OrgMemberModel])
async def list_organization_members(
    member_id: UUID | None = Query(None, alias="id", description="Identifier of the employee to retrieve."),
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> list[OrgMemberModel]:
    token = credentials.credentials
    return await UserOrganizationService.list_members(token, member_id)
