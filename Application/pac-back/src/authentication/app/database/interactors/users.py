from uuid import UUID

from app.database.client import get_db
from app.database.interactors.authentication import AuthenticationInteractor
from app.models.base_models import StatusResponse, UserListModel, UserModificationModel
from app.models.enum_models import RoleEnum
from fastapi import HTTPException, status
from supabase import Client


class UsersInteractor:
    @staticmethod
    async def get_user_from_user_id(user_id: UUID) -> UserListModel:
        supabase: Client = get_db()
        response = supabase.table("users").select("*").eq("id", user_id).limit(1).execute()
        return UserListModel(**response.data[0])

    @staticmethod
    async def get_role(user_id: UUID) -> RoleEnum:
        db_user = await UsersInteractor.get_user_from_user_id(user_id)
        return db_user.role

    @staticmethod
    async def modify_user(user_id: UUID, user: UserModificationModel):
        supabase: Client = get_db()
        modifications = {}
        if user.first_name is not None:
            modifications["first_name"] = user.first_name
        if user.last_name is not None:
            modifications["last_name"] = user.last_name
        if user.email is not None:
            modifications["email"] = user.email
        response = supabase.table("users").update(modifications).eq("id", user_id).execute()
        return UserListModel(**response.data[0])

    @staticmethod
    async def change_user_password(user_id: UUID, current_password: str, new_password: str) -> StatusResponse:
        supabase: Client = get_db()
        response = supabase.table("users").select("password").eq("id", user_id).execute()
        if not response.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

        current_hashed_password = response.data[0]["password"]
        is_valid = await AuthenticationInteractor.verify_password(current_password, current_hashed_password)

        if not is_valid:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")

        new_hashed_password = await AuthenticationInteractor.password_hasher(new_password)
        supabase.table("users").update({"password": new_hashed_password}).eq("id", user_id).execute()
        return StatusResponse(status="ok", message="Successfully updated user's password.")
