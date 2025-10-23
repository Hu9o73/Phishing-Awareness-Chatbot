from uuid import UUID

from app.database.client import get_db
from app.database.interactors.Base.users import UsersInteractor
from app.models.base_models import PublicUserModel
from app.models.enum_models import RoleEnum
from fastapi import HTTPException, status
from supabase import Client


class UsersService:
    @staticmethod
    async def get_user_from_id(user_id: UUID) -> PublicUserModel:
        return await UsersInteractor.get_user_from_id(user_id=user_id)
