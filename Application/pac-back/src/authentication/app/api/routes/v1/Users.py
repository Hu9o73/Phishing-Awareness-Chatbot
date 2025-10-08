from app.database.interactors.authentication import AuthenticationInteractor
from app.database.interactors.users import UsersInteractor
from app.Middleware import Middleware
from app.models.base_models import StatusResponse, UserListModel, UserModificationModel
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

router = APIRouter()
security = HTTPBearer()


@router.get("/user", response_model=list[UserListModel], dependencies=[Depends(Middleware.token_required)])
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    token_decoded = await AuthenticationInteractor.decode_jwt(token)
    return await UsersInteractor.get_user_from_user_id(token_decoded.user_id)


@router.put("/user", response_model=UserListModel, dependencies=[Depends(Middleware.token_required)])
async def modify_user(user: UserModificationModel, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    token_decoded = await AuthenticationInteractor.decode_jwt(token)
    return await UsersInteractor.modify_user(token_decoded.user_id, user)


@router.put("/user/password", response_model=StatusResponse, dependencies=[Depends(Middleware.token_required)])
async def change_user_password(
    current_password: str, new_password: str, credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    token_decoded = await AuthenticationInteractor.decode_jwt(token)
    return await UsersInteractor.change_user_password(token_decoded.user_id, current_password, new_password)
