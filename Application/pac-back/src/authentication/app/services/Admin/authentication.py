from uuid import UUID

from app.database.client import get_db
from app.database.interactors.Base.authentication import AuthenticationInteractor
from app.database.interactors.Admin.authentication import AdminAuthenticationInteractor
from app.database.interactors.Admin.organization import AdminOrganizationInteractor
from app.services.Base.authentication import AuthenticationService
from app.models.base_models import PublicUserModel, StatusResponse, UserCreationModel, UserModel
from app.models.enum_models import RoleEnum
from fastapi import HTTPException, status
from supabase import Client


class AdminAuthenticationService(AuthenticationService):
    @staticmethod
    async def create_user(user: UserCreationModel) -> UserModel:
        # Check if email already exists
        email_check = await AuthenticationInteractor.get_user_id_from_email(user.email)
        if email_check.data:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

        # Check has org id if role isn't admin
        if user.role != RoleEnum.ADMIN:
            if user.organization_id is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User must have an organization_id")

        # Check org exists if org id
        if user.organization_id is not None:
            user_org = await AdminOrganizationInteractor.list_organizations(org_id=user.organization_id)
            if len(user_org) == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")

        # Hash the password
        hashed_password = await AuthenticationService.password_hasher(user.password)
        user.password = hashed_password

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
