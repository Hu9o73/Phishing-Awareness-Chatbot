from abc import ABC

import requests
from app.common.settings import settings


class AuthenticationInteractor(ABC):
    @staticmethod
    def login(email: str, password: str):
        payload = {
            "email": email,
            "password": password,
        }
        return requests.post(url=f"{settings.AUTHENTICATION_URL}/auth/login", params=payload)

    @staticmethod
    def verifyjwt(token: str | None):
        if token:
            headers = {"Authorization": f"Bearer {token}"}
        else:
            headers = {}
        return requests.post(url=f"{settings.AUTHENTICATION_URL}/auth/verifyjwt", headers=headers)
