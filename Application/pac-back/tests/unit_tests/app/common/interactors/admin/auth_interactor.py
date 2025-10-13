from uuid import UUID

import requests
from app.common.enum_models import RoleEnum
from app.common.interactors.base.auth_interactor import AuthenticationInteractor
from app.common.settings import settings


class AdminAuthenticationInteractor(AuthenticationInteractor):
    @staticmethod
    def create_user(
        token: str,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        role: RoleEnum,
        org_id: UUID | None = None
    ):
        headers = {"Authorization": f"Bearer {token}"}
        payload = {
            "email": email,
            "password": password,
            "recaptcha_token": "mytoken",
            "first_name": first_name,
            "last_name": last_name,
            "role": str(role.value),
            "organization_id": org_id,
        }

        return requests.post(url=f"{settings.AUTHENTICATION_URL}/admin/user", params=payload, headers=headers)
