from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.Middleware import Middleware
from app.models.base_models import OrgMemberModel
from app.services.User.organization import UserOrganizationService

router = APIRouter()
security = HTTPBearer()


@router.get("/organization/members", response_model=list[OrgMemberModel])
async def list_organization_members(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> list[OrgMemberModel]:
    token = credentials.credentials
    return await UserOrganizationService.list_members(token)
