import bcrypt
from app.common.base_models import UserModel
from app.common.database.client import get_db
from app.common.enum_models import RoleEnum
from app.common.interactors.base.auth_interactor import AuthenticationInteractor
from supabase import Client


class HackAuthenticationInteractor(AuthenticationInteractor):
    @staticmethod
    def _password_hasher(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    @staticmethod
    def delete_using_email(email: str):
        supabase: Client = get_db()
        return supabase.table("users").delete().eq("email", email).execute()

    @staticmethod
    def create_an_admin(first_name: str, last_name: str, email: str, password: str):
        supabase = get_db()
        response = (
            supabase.table("users")
            .insert(
                {
                    "email": email,
                    "password": HackAuthenticationInteractor._password_hasher(password),
                    "role": RoleEnum.ADMIN,
                    "first_name": first_name,
                    "last_name": last_name,
                }
            )
            .execute()
        )

        return UserModel(**response.data[0])
