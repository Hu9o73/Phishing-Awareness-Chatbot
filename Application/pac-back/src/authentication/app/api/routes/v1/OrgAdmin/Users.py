
from app.api.routes.v1.AuthenticationRoutes import verify_recaptcha
from app.database.interactors.OrgAdmin.authentication import OrgAdminAuthenticationInteractor
from app.models.base_models import UserCreationModel, UserModel
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
    recaptcha_token: str,
):
    # Verify reCAPTCHA first
    if not await verify_recaptcha(recaptcha_token):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="reCAPTCHA verification failed. Please try again."
        )
    user = UserCreationModel(email=email, password=password, first_name=first_name, last_name=last_name)
    return await OrgAdminAuthenticationInteractor.create_user(user)
