from app.database.interactors.Base.authentication import AuthenticationInteractor
from app.database.interactors.Base.users import UsersInteractor
from app.Middleware import Middleware
from app.models.base_models import UserListModel
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

router = APIRouter()
security = HTTPBearer()


@router.get("/user", response_model=UserListModel, dependencies=[Depends(Middleware.token_required)])
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    token_decoded = await AuthenticationInteractor.decode_jwt(token)
    return await UsersInteractor.get_user_from_id(token_decoded.user_id)
