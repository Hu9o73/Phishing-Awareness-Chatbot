from uuid import UUID

from app.database.client import get_db
from app.models.base_models import UserListModel
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
    async def get_user_from_id(user_id: UUID) -> UserListModel:
        supabase: Client = get_db()
        response = supabase.table("users").select("*").eq("id", user_id).limit(1).execute()
        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
        return UserListModel(**response.data[0])
