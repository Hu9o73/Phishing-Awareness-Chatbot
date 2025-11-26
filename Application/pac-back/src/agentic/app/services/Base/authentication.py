import os

import dotenv
import requests
from app.models.base_models import JWTModel, PublicUserModel
from app.models.enum_models import RoleEnum
from fastapi import HTTPException, status
from requests import RequestException

dotenv.load_dotenv()


class AuthenticationService:
    """Client used to interact with the authentication service from the agentic service."""

    _DEFAULT_BASE_URL = "http://pac-authentication:8001"

    @staticmethod
    def _build_url(path: str) -> str:
        base_url = os.getenv("AUTH_SERVICE_URL", AuthenticationService._DEFAULT_BASE_URL)
        return f"{base_url.rstrip('/')}{path}"

    @staticmethod
    def verify_jwt(token: str) -> JWTModel:
        url = AuthenticationService._build_url("/auth/verifyjwt")
        try:
            response = requests.post(url, headers={"Authorization": f"Bearer {token}"}, timeout=5.0)
        except RequestException as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Authentication service is unavailable",
            ) from exc

        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=AuthenticationService._extract_detail(response),
            ) from exc

        try:
            payload = response.json()
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Invalid response from authentication service",
            ) from exc

        return JWTModel(**payload)

    @staticmethod
    def get_current_user(token: str) -> PublicUserModel:
        url = AuthenticationService._build_url("/auth/user")
        try:
            response = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=5.0)
        except RequestException as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Authentication service is unavailable",
            ) from exc

        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=AuthenticationService._extract_detail(response),
            ) from exc

        try:
            payload = response.json()
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Invalid response from authentication service",
            ) from exc
        return PublicUserModel(**payload)

    @staticmethod
    def get_user_role(token: str) -> RoleEnum | None:
        user = AuthenticationService.get_current_user(token)
        role = user.role
        if role is None:
            return None
        try:
            return RoleEnum(role)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Received unknown role from authentication service",
            ) from exc

    @staticmethod
    def _extract_detail(response: requests.Response) -> str:
        detail = "Authentication service request failed"
        try:
            payload = response.json()
            if isinstance(payload, dict):
                detail = payload.get("detail", detail)
        except ValueError:
            pass
        return detail
