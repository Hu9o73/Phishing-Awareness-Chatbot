import requests
from app.common.interactors.base.auth_interactor import AuthenticationInteractor
from app.common.settings import settings


class AdminAuthenticationInteractor(AuthenticationInteractor):
    def create_user(self, first_name: str, last_name: str, email: str, password: str):
        payload = {
            "email": email,
            "password": password,
            "recaptcha_token": "mytoken",
            "first_name": first_name,
            "last_name": last_name,
        }

        return requests.post(url=f"{settings.AUTHENTICATION_URL}/orgadmin/user", params=payload)
