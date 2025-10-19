from uuid import UUID

from app.api.routes.v1.AuthenticationRoutes import verify_recaptcha
from app.database.interactors.OrgAdmin.authentication import OrgAdminAuthenticationInteractor
from app.models.base_models import PublicUserModel, StatusResponse, UserCreationModel, UserModel
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

router = APIRouter()
security = HTTPBearer()

@router.post("/user", response_model=UserModel)
async def create_user(
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    recaptcha_token: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    # Verify reCAPTCHA first
    if not await verify_recaptcha(recaptcha_token):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="reCAPTCHA verification failed. Please try again."
        )
    user = UserCreationModel(email=email, password=password, first_name=first_name, last_name=last_name)
    token = credentials.credentials
    return await OrgAdminAuthenticationInteractor.create_user(token, user)


@router.get("/users", response_model=list[PublicUserModel])
async def list_users_in_org(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """List all non-admin users in orgadmin's organization."""
    token = credentials.credentials
    return await OrgAdminAuthenticationInteractor.list_users_org(token)


@router.delete("/user", response_model=StatusResponse)
async def delete_user_by_id(user_id: UUID, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    return await OrgAdminAuthenticationInteractor.delete_user_by_id(token, user_id)
