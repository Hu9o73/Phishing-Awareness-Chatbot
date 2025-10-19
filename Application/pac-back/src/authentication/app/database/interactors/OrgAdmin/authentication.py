from uuid import UUID

from app.database.client import get_db
from app.database.interactors.Base.authentication import AuthenticationInteractor
from app.models.base_models import PublicUserModel, StatusResponse, UserCreationModel, UserModel
from app.models.enum_models import RoleEnum
from fastapi import HTTPException, status
from supabase import Client


class OrgAdminAuthenticationInteractor(AuthenticationInteractor):
    @staticmethod
    async def create_user(token: str, user: UserCreationModel) -> UserModel:
        supabase: Client = get_db()
        org_id = await AuthenticationInteractor.get_user_org(token)

        # Check if email already exists
        email_check = supabase.table("users").select("id").eq("email", user.email).limit(1).execute()
        if email_check.data:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

        # Hash the password
        hashed_password = await AuthenticationInteractor.password_hasher(user.password)

        # Insert new user
        response = (
            supabase.table("users")
            .insert(
                {
                    "email": user.email,
                    "password": hashed_password,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "organization_id": org_id,
                }
            )
            .execute()
        )

        return UserModel(**response.data[0])

    @staticmethod
    async def list_users_org(token: str) -> list[PublicUserModel]:
        supabase: Client = get_db()
        org_id = await AuthenticationInteractor.get_user_org(token)
        response = supabase.table("users").select("*").eq("organization_id", org_id).execute()
        all_users = [PublicUserModel(**user) for user in response.data]
        return [user for user in all_users if user.role == RoleEnum.MEMBER]

    @staticmethod
    async def delete_user_by_id(token: str, user_id: UUID) -> StatusResponse:
        supabase: Client = get_db()
        org_id = await AuthenticationInteractor.get_user_org(token)
        # Safety check
        response = supabase.table("users").select("id").eq("id", user_id).eq("organization_id", org_id).execute()
        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found.")
        supabase.table("users").delete().eq("id", user_id).eq("organization_id", org_id).execute()
        return StatusResponse(status="ok", message=f"Delete user with id {user_id}")
