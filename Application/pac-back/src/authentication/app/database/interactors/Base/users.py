from uuid import UUID

from app.database.client import get_db
from app.models.base_models import PublicUserModel
from app.models.enum_models import RoleEnum
from fastapi import HTTPException, status
from supabase import Client


class UsersInteractor:
    @staticmethod
    async def get_user_from_id(user_id: UUID) -> PublicUserModel | None:
        supabase: Client = get_db()
        response = supabase.table("users").select("*").eq("id", user_id).limit(1).execute()
        return PublicUserModel(**response.data[0]) if response.data and len(response.data) > 0 else None
