from uuid import UUID

from app.database.interactors.Base.users import UsersInteractor
from app.database.interactors.OrgAdmin.authentication import OrgAdminAuthenticationInteractor
from app.models.base_models import PublicUserModel, StatusResponse, UserCreationModel, UserModel
from app.models.enum_models import RoleEnum
from app.services.Base.authentication import AuthenticationService
from fastapi import HTTPException, status


class OrgAdminAuthenticationService(AuthenticationService):
    @staticmethod
    async def create_user(token: str, email: str, first_name: str, last_name: str, password: str) -> UserModel:
        jwt_decoded = await AuthenticationService.decode_jwt(token)
        orgadmin_user = await UsersInteractor.get_user_from_id(jwt_decoded.user_id)

        # Check if user exists
        await UsersInteractor.check_if_user_exists(email)

        # Hash the password
        hashed_password = await AuthenticationService.password_hasher(password)

        user_to_insert = UserCreationModel(
            email=email,
            hashed_password=hashed_password,
            first_name=first_name,
            last_name=last_name,
            role=RoleEnum.MEMBER,
            organization_id=orgadmin_user.organization_id,
        )

        return await OrgAdminAuthenticationInteractor.create_user(user_to_insert)

    @staticmethod
    async def list_member_users_in_org(token: str) -> list[PublicUserModel]:
        jwt_decoded = await AuthenticationService.decode_jwt(token)
        user = await UsersInteractor.get_user_from_id(jwt_decoded.user_id)
        all_users = await OrgAdminAuthenticationInteractor.list_users_org(user.organization_id)

        return [user for user in all_users if user.role == RoleEnum.MEMBER]

    @staticmethod
    async def delete_user_by_id(token: str, user_id: UUID) -> StatusResponse:
        jwt_decoded = await AuthenticationService.decode_jwt(token)

        orgadmin_user = await UsersInteractor.get_user_from_id(jwt_decoded.user_id)
        user = await UsersInteractor.get_user_from_id(user_id)

        if orgadmin_user.organization_id != user.organization_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found.")

        return await OrgAdminAuthenticationInteractor.delete_user_by_id(user_id)
