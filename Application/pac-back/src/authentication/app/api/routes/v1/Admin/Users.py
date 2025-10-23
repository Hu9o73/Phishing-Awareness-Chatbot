from uuid import UUID

from app.api.routes.v1.AuthenticationRoutes import verify_recaptcha
from app.models.base_models import PublicUserModel, StatusResponse, UserModel
from app.models.enum_models import RoleEnum
from app.services.Admin.authentication import AdminAuthenticationService
from fastapi import APIRouter, HTTPException, status
from fastapi.security import HTTPBearer

router = APIRouter()
security = HTTPBearer()

@router.post("/user", response_model=UserModel)
async def create_user(
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    role: RoleEnum,
    recaptcha_token: str,
    organization_id: UUID | None = None,
):
    # Verify reCAPTCHA first
    if not await verify_recaptcha(recaptcha_token):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="reCAPTCHA verification failed. Please try again."
        )
    return await AdminAuthenticationService.create_user(email, password, first_name, last_name, role, organization_id)


@router.delete("/user", response_model=StatusResponse)
async def delete_user(user_id: UUID):
    return await AdminAuthenticationService.delete_user(user_id)


@router.get("/user/orgadmins", response_model=list[PublicUserModel])
async def list_orgadmins(organization_id: UUID):
    return await AdminAuthenticationService.list_org_admins(organization_id)
