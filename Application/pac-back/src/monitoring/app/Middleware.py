import os

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.models.base_models import JWTModel
from app.models.enum_models import RoleEnum
from app.services.Base.authentication import AuthenticationService

security = HTTPBearer(auto_error=False)


class Middleware:
    @staticmethod
    async def token_required(
        request: Request, credentials: HTTPAuthorizationCredentials | None = Depends(security)
    ):
        if Middleware._is_super_clock_request(request):
            return
        if credentials is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing credentials.")
        token = credentials.credentials
        token_decoded = AuthenticationService.verify_jwt(token)
        if not isinstance(token_decoded, JWTModel):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid JWT token")

    @staticmethod
    async def is_admin(
        request: Request, credentials: HTTPAuthorizationCredentials | None = Depends(security)
    ):
        if Middleware._is_super_clock_request(request):
            return
        if credentials is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing credentials.")
        token = credentials.credentials
        user_status = Middleware._extract_status_from_jwt(token)
        if user_status != RoleEnum.ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not admin.")

    @staticmethod
    async def is_org_admin(
        request: Request, credentials: HTTPAuthorizationCredentials | None = Depends(security)
    ):
        if Middleware._is_super_clock_request(request):
            return
        if credentials is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing credentials.")
        token = credentials.credentials
        user_status = Middleware._extract_status_from_jwt(token)
        if user_status != RoleEnum.ORG_ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not admin of his organization.")

    @staticmethod
    async def is_user(
        request: Request, credentials: HTTPAuthorizationCredentials | None = Depends(security)
    ):
        if Middleware._is_super_clock_request(request):
            return
        if credentials is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing credentials.")
        token = credentials.credentials
        user_status = Middleware._extract_status_from_jwt(token)
        if user_status != RoleEnum.MEMBER:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User does not have member role.")

    @staticmethod
    def _extract_status_from_jwt(jwt_str: str) -> RoleEnum | None:
        decoded_jwt = AuthenticationService.verify_jwt(jwt_str)
        if decoded_jwt.user_id:
            return AuthenticationService.get_user_role(jwt_str)
        return None

    @staticmethod
    def _is_super_clock_request(request: Request) -> bool:
        expected = os.getenv("SUPER_CLOCK_TOKEN")
        if not expected:
            return False
        provided = request.headers.get("X-Super-Clock-Token")
        if provided != expected:
            return False
        return request.url.path in ("/retrieve-answers", "/send-all-pending", "/send-all-pending-emails")
