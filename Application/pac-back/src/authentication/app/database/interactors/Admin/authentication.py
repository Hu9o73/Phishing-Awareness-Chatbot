from uuid import UUID

from app.database.client import get_db
from app.database.interactors.Base.authentication import AuthenticationInteractor
from app.models.base_models import PublicUserModel, UserCreationModel, UserModel
from app.models.enum_models import RoleEnum
from fastapi import HTTPException, status
from supabase import Client


class AdminAuthenticationInteractor(AuthenticationInteractor):
    @staticmethod
    async def create_user(user: UserCreationModel) -> UserModel:
        supabase: Client = get_db()

        # Check if email already exists
        email_check = supabase.table("users").select("id").eq("email", user.email).limit(1).execute()
        if email_check.data:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

        # Check has org id if role isn't admin
        if user.role != RoleEnum.ADMIN:
            if user.organization_id is None or not isinstance(user.organization_id, UUID):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User must have an organization_id")

        # Check org exists if org id
        if user.organization_id is not None:
            org_check = (
                supabase.table("organizations").select("id").eq("id", str(user.organization_id)).limit(1).execute()
            )
            if not org_check.data or len(org_check.data) == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")

        # Hash the password
        hashed_password = await AuthenticationInteractor.password_hasher(user.password)

        # Insert new user
        response = (
            supabase.table("users")
            .insert(
                {
                    "email": user.email,
                    "password": hashed_password,
                    "role": user.role,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "organization_id": str(user.organization_id),
                }
            )
            .execute()
        )

        return UserModel(**response.data[0])

    @staticmethod
    async def list_org_admins():
        supabase: Client = get_db()
        response = supabase.table("users").select("*").eq("role", RoleEnum.ORG_ADMIN.value).execute()
        return [PublicUserModel(**user) for user in response.data]
