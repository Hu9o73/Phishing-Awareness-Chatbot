from uuid import UUID

from app.database.client import get_db
from app.database.interactors.Base.authentication import AuthenticationInteractor
from app.services.Base.authentication import AuthenticationService
from app.models.base_models import PublicUserModel, StatusResponse, UserCreationModel, UserModel
from app.models.enum_models import RoleEnum
from fastapi import HTTPException, status
from supabase import Client


class AdminAuthenticationInteractor(AuthenticationInteractor):
    @staticmethod
    async def create_user(user: UserCreationModel) -> UserModel:
        supabase: Client = get_db()
        response = (
            supabase.table("users")
            .insert(
                {
                    "email": user.email,
                    "password": user.password,
                    "role": user.role,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "organization_id": str(user.organization_id) if user.organization_id else None,
                }
            )
            .execute()
        )

        return UserModel(**response.data[0])

    @staticmethod
    async def list_org_admins(organization_id: UUID) -> list[PublicUserModel]:
        supabase: Client = get_db()
        response = (
            supabase.table("users")
            .select("*")
            .eq("role", RoleEnum.ORG_ADMIN.value)
            .eq("organization_id", organization_id)
            .execute()
        )
        return [PublicUserModel(**user) for user in response.data]

    @staticmethod
    async def delete_user(user_id: UUID):
        supabase: Client = get_db()
        supabase.table("users").delete().eq("id", user_id).execute()
        return StatusResponse(status="ok", message=f"Successfully delete user with id {user_id}")
