from uuid import UUID

from app.database.client import get_db
from app.database.interactors.Base.authentication import AuthenticationInteractor
from app.models.base_models import PublicUserModel, StatusResponse, UserCreationModel, UserModel
from supabase import Client


class OrgAdminAuthenticationInteractor(AuthenticationInteractor):
    @staticmethod
    async def create_user(user: UserCreationModel) -> UserModel:
        supabase: Client = get_db()
        response = (
            supabase.table("users").insert(
                {
                    "email": user.email,
                    "password": user.hashed_password,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role,
                    "organization_id": str(user.organization_id),
                }
            ).execute()
        )
        return UserModel(**response.data[0])

    @staticmethod
    async def list_users_org(org_id: UUID) -> list[PublicUserModel]:
        supabase: Client = get_db()
        response = supabase.table("users").select("*").eq("organization_id", org_id).execute()
        return [PublicUserModel(**user) for user in response.data]

    @staticmethod
    async def delete_user_by_id(user_id: UUID) -> StatusResponse:
        supabase: Client = get_db()
        supabase.table("users").delete().eq("id", user_id).execute()
        return StatusResponse(status="ok", message=f"Delete user with id {user_id}")
