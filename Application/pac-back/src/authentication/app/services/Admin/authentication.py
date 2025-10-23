from uuid import UUID

from app.database.interactors.Admin.authentication import AdminAuthenticationInteractor
from app.database.interactors.Admin.organization import AdminOrganizationInteractor
from app.database.interactors.Base.users import UsersInteractor
from app.models.base_models import PublicUserModel, StatusResponse, UserCreationModel, UserModel
from app.models.enum_models import RoleEnum
from app.services.Base.authentication import AuthenticationService
from fastapi import HTTPException, status


class AdminAuthenticationService(AuthenticationService):
    @staticmethod
    async def create_user(
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        role: RoleEnum,
        organization_id: UUID | None = None,
    ) -> UserModel:
        # Check if email already exists
        await UsersInteractor.check_if_user_exists(email)

        # Check has org id if role isn't admin
        if role != RoleEnum.ADMIN:
            if organization_id is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User must have an organization_id")

        # Check org exists if org id
        if organization_id is not None:
            user_org = await AdminOrganizationInteractor.list_organizations(org_id=organization_id)
            if len(user_org) == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")

        # Hash the password
        hashed_password = await AuthenticationService.password_hasher(password)

        user = UserCreationModel(
            email=email,
            hashed_password=hashed_password,
            first_name=first_name,
            last_name=last_name,
            role=role,
            organization_id=organization_id,
        )

        # Insert new user
        new_user = await AdminAuthenticationInteractor.create_user(user)

        return new_user

    @staticmethod
    async def list_org_admins(organization_id: UUID) -> list[PublicUserModel]:
        org_check = await AdminOrganizationInteractor.list_organizations(org_id=organization_id)
        if len(org_check) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")

        return await AdminAuthenticationInteractor.list_org_admins(organization_id)

    @staticmethod
    async def delete_user(user_id: UUID) -> StatusResponse:
        return await AdminAuthenticationInteractor.delete_user(user_id)
