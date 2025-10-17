import os

import requests
from app.database.interactors.Base.authentication import AuthenticationInteractor
from app.Middleware import Middleware
from app.models.base_models import JWTModel, LoginResponse
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

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


@router.post("/login", response_model=LoginResponse)
async def login(email: str, password: str):
    return await AuthenticationInteractor.login_user(email, password)


@router.post("/verifyjwt", response_model=JWTModel, dependencies=[Depends(Middleware.token_required)])
async def check_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    return await AuthenticationInteractor.decode_jwt(token)
