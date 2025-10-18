from uuid import UUID

from app.database.client import get_db
from app.models.base_models import PublicUserModel
from app.models.enum_models import RoleEnum
from fastapi import HTTPException, status
from supabase import Client


class UsersInteractor:
    @staticmethod
    async def get_user_organization_from_id(user_id: UUID) -> str:
        supabase: Client = get_db()
        response = supabase.table("users").select("organization_id").eq("id", user_id).limit(1).execute()
        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
        return response.data[0]["organization_id"]

    @staticmethod
    async def get_user_from_id(user_id: UUID) -> PublicUserModel:
        supabase: Client = get_db()
        response = supabase.table("users").select("*").eq("id", user_id).limit(1).execute()
        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
        return PublicUserModel(**response.data[0])

    @staticmethod
    async def get_role(user_id: UUID) -> RoleEnum:
        supabase: Client = get_db()
        response = supabase.table("users").select("role").eq("id", user_id).limit(1).execute()
        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
        return RoleEnum(response.data[0]["role"])
