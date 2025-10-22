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

    @staticmethod
    def delete_user(token: str, user_id: UUID):
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"user_id": user_id}
        return requests.delete(url=f"{settings.AUTHENTICATION_URL}/admin/user", params=payload, headers=headers)

    @staticmethod
    def list_orgadmins(token: str, org_id: UUID):
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"organization_id": org_id}
        return requests.get(url=f"{settings.AUTHENTICATION_URL}/admin/user/orgadmins", params=payload, headers=headers)

    @staticmethod
    def create_org(token: str, organization_name: str, organization_description: str | None = None):
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"organization_name": organization_name, "organization_description": organization_description}
        return requests.post(url=f"{settings.AUTHENTICATION_URL}/admin/organization", params=payload, headers=headers)

    @staticmethod
    def list_all_orgs(token: str):
        headers = {"Authorization": f"Bearer {token}"}
        return requests.get(url=f"{settings.AUTHENTICATION_URL}/admin/organizations", headers=headers)

    @staticmethod
    def delete_org(token: str, org_id: UUID):
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"organization_id": org_id}
        return requests.delete(url=f"{settings.AUTHENTICATION_URL}/admin/organization", params=payload, headers=headers)
