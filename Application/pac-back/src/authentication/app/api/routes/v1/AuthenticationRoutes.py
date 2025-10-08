import os

import requests
from app.database.interactors.authentication import AuthenticationInteractor
from app.Middleware import Middleware
from app.models.base_models import UserCreationModel, UserModel, LoginResponse, JWTModel
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import ExpiredSignatureError, InvalidTokenError

router = APIRouter()
security = HTTPBearer()


async def verify_recaptcha(token: str) -> bool:
    if not token:
        return False

    secret_key = os.getenv("RECAPTCHA_SECRET_KEY")
    if not secret_key:
        # If no secret key is configured, skip reCAPTCHA verification in development
        return True

    try:
        response = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={"secret": secret_key, "response": token},
            timeout=10,
        )

        result = response.json()
        return result.get("success", False)

    except requests.RequestException as e:
        print(f"reCAPTCHA verification error: {e}")
        return False


@router.post("/signup", response_model=UserModel)
async def signup(
    email: str,
    password: str,
    recaptcha_token: str,
    first_name: str,
    last_name: str,
):
    # Verify reCAPTCHA first
    if not await verify_recaptcha(recaptcha_token):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="reCAPTCHA verification failed. Please try again."
        )
    user = UserCreationModel(email=email, password=password, first_name=first_name, last_name=last_name)
    return await AuthenticationInteractor.create_user(user)


@router.post("/login", response_model=LoginResponse)
async def login(email: str, password: str):
    return await AuthenticationInteractor.login_user(email, password)


@router.post("/verifyjwt", response_model=JWTModel, dependencies=[Depends(Middleware.token_required)])
async def check_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    return await AuthenticationInteractor.decode_jwt(token)
