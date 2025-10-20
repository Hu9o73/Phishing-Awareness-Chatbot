from uuid import UUID

from app.api.routes.v1.AuthenticationRoutes import verify_recaptcha
from app.database.interactors.Admin.authentication import AdminAuthenticationInteractor
from app.models.base_models import PublicUserModel, StatusResponse, UserCreationModel, UserModel
from app.models.enum_models import RoleEnum
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
    role = RoleEnum(role)
    user = UserCreationModel(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        role=role,
        organization_id=organization_id,
    )
    return await AdminAuthenticationInteractor.create_user(user)


@router.delete("/user", response_model=StatusResponse)
async def delete_user(user_id: UUID):
    return await AdminAuthenticationInteractor.delete_user(user_id)


@router.get("/user/orgadmins", response_model=list[PublicUserModel])
async def list_orgadmins(organization_id: UUID):
    return await AdminAuthenticationInteractor.list_org_admins(organization_id)
