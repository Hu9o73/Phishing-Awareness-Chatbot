from uuid import UUID

from supabase import Client
import requests

from app.common.settings import settings
from app.common.database.client import get_db

class AuthenticationInteractor():
    def login(self, email: str, password: str):
        payload = {
            "email": email,
            "password": password,
        }
        return requests.post(url=f"{settings.AUTHENTICATION_URL}/auth/login", params=payload)

    def signup(self, first_name: str, last_name: str, email: str, password: str):
        payload = {
            "email": email,
            "password": password,
            "recaptcha_token": "mytoken",
            "first_name": first_name,
            "last_name": last_name,
        }

        return requests.post(url=f"{settings.AUTHENTICATION_URL}/auth/signup", params=payload)

    def delete(self, email: UUID):
        supabase: Client = get_db()
        return supabase.table("users").delete().eq("email", email).execute()


    def verifyjwt(self, token: str | None):
        if token:
            headers = {"Authorization": f"Bearer {token}"}
        else:
            headers = {}
        return requests.post(url=f"{settings.AUTHENTICATION_URL}/auth/verifyjwt", headers=headers)
