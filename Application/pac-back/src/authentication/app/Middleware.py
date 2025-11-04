from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.database.interactors.Base.users import UsersInteractor
from app.models.base_models import JWTModel
from app.models.enum_models import RoleEnum
from app.services.Base.authentication import AuthenticationService

security = HTTPBearer()


class Middleware:
    @staticmethod
    async def token_required(credentials: HTTPAuthorizationCredentials = Depends(security)):
        token = credentials.credentials
        token_decoded = await AuthenticationService.decode_jwt(token)
        if not isinstance(token_decoded, JWTModel):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid JWT token")

    @staticmethod
    async def is_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
        token = credentials.credentials
        user_status = await Middleware._extract_status_from_jwt(token)
        if user_status != RoleEnum.ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not admin.")

    @staticmethod
    async def is_org_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
        token = credentials.credentials
        user_status = await Middleware._extract_status_from_jwt(token)
        if user_status != RoleEnum.ORG_ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not admin of his organization.")

    @staticmethod
    async def _extract_status_from_jwt(jwt_str: str):
        decoded_jwt = await AuthenticationService.decode_jwt(jwt_str)
        if decoded_jwt.user_id:
            user = await UsersInteractor.get_user_from_id(decoded_jwt.user_id)
            return user.role
        return None
