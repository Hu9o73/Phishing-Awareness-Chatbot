from uuid import UUID

from app.database.client import get_db
from app.models.base_models import PublicUserModel
from app.models.enum_models import RoleEnum
from fastapi import HTTPException, status
from supabase import Client


class UsersInteractor:
    @staticmethod
    async def get_user_from_id(user_id: UUID) -> PublicUserModel:
        supabase: Client = get_db()
        response = supabase.table("users").select("*").eq("id", user_id).limit(1).execute()
        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return PublicUserModel(**response.data[0])

    @staticmethod
    async def check_if_user_exists(email: str) -> None:
        supabase: Client = get_db()
        response = supabase.table("users").select("id").eq("email", email).limit(1).execute()
        if response.data and len(response.data) > 0:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
        return None
