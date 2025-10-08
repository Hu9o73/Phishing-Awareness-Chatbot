
from app.api.routes.v1.AuthenticationRoutes import verify_recaptcha
from app.database.interactors.Admin.authentication import AdminAuthenticationInteractor
from app.models.base_models import UserCreationModel, UserModel
from app.models.enum_models import RoleEnum
from fastapi import APIRouter, HTTPException, status
from fastapi.security import HTTPBearer

router = APIRouter()
security = HTTPBearer()

@router.post("/user", response_model=UserModel)
async def create_user(
    email: str,
    password: str,
    recaptcha_token: str,
    first_name: str,
    last_name: str,
    role: RoleEnum,
):
    # Verify reCAPTCHA first
    if not await verify_recaptcha(recaptcha_token):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="reCAPTCHA verification failed. Please try again."
        )
    role = RoleEnum(role)
    user = UserCreationModel(email=email, password=password, first_name=first_name, last_name=last_name, role=role)
    return await AdminAuthenticationInteractor.create_user(user)
