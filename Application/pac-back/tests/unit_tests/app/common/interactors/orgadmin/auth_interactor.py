from uuid import UUID

import requests
from app.common.interactors.base.auth_interactor import AuthenticationInteractor
from app.common.settings import settings


class OrgAdminAuthenticationInteractor(AuthenticationInteractor):
    @staticmethod
    def create_user(token: str, first_name: str, last_name: str, email: str, password: str):
        headers = {"Authorization": f"Bearer {token}"}
        payload = {
            "email": email,
            "password": password,
            "recaptcha_token": "mytoken",
            "first_name": first_name,
            "last_name": last_name,
        }

        return requests.post(url=f"{settings.AUTHENTICATION_URL}/orgadmin/user", params=payload, headers=headers)

    @staticmethod
    def delete_user(token: str, user_id: str):
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"user_id": user_id}
        return requests.delete(url=f"{settings.AUTHENTICATION_URL}/orgadmin/user", params=payload, headers=headers)

    @staticmethod
    def list_users(token: str):
        headers = {"Authorization": f"Bearer {token}"}
        return requests.get(url=f"{settings.AUTHENTICATION_URL}/orgadmin/users", headers=headers)

    @staticmethod
    def create_member(token: str, first_name: str, last_name: str, email: str):
        headers = {"Authorization": f"Bearer {token}"}
        payload = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
        }
        return requests.post(url=f"{settings.AUTHENTICATION_URL}/orgadmin/member", params=payload, headers=headers)

    @staticmethod
    def get_member_by_id(token: str, member_id: UUID):
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"member_id": str(member_id)}
        return requests.get(url=f"{settings.AUTHENTICATION_URL}/orgadmin/member", params=payload, headers=headers)

    @staticmethod
    def get_members_in_org(token: str):
        headers = {"Authorization": f"Bearer {token}"}
        return requests.get(url=f"{settings.AUTHENTICATION_URL}/orgadmin/members", headers=headers)

    @staticmethod
    def delete_member_by_id(token: str, member_id: UUID):
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"member_id": member_id}
        return requests.delete(url=f"{settings.AUTHENTICATION_URL}/orgadmin/member", params=payload, headers=headers)
