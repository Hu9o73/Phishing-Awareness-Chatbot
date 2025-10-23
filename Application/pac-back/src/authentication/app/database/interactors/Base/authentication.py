from abc import ABC, abstractmethod
from uuid import UUID

from app.database.client import get_db
from app.models.base_models import UserCreationModel, UserModel
from supabase import Client


class AuthenticationInteractor(ABC):
    @staticmethod
    async def fetch_hashed_password(email: str):
        supabase: Client = get_db()
        return supabase.table("users").select("id, password").eq("email", email).limit(1).execute()

    @staticmethod
    async def get_user_org(user_id: UUID):
        supabase: Client = get_db()
        return supabase.table("users").select("organization_id").eq("id", user_id).limit(1).execute()

    @staticmethod
    async def get_user_id_from_email(email: str):
        supabase: Client = get_db()
        return supabase.table("users").select("id").eq("email", email).limit(1).execute()

    @staticmethod
    @abstractmethod
    async def create_user(user: UserCreationModel) -> UserModel:
        pass
