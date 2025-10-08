from app.database.client import get_db
from app.database.interactors.Base.authentication import AuthenticationInteractor
from app.models.base_models import UserCreationModel, UserModel
from fastapi import HTTPException, status
from supabase import Client


class AdminAuthenticationInteractor(AuthenticationInteractor):
    @staticmethod
    async def create_user(user: UserCreationModel) -> UserModel:
        supabase: Client = get_db()

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
                }
            )
            .execute()
        )

        return UserModel(**response.data[0])
