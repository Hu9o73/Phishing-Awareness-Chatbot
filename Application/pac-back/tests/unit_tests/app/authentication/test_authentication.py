from uuid import UUID, uuid4

import pytest
from app.common.base_models import UserModel
from app.common.enum_models import RoleEnum
from app.common.interactors.admin.auth_interactor import AdminAuthenticationInteractor
from app.common.interactors.base.auth_interactor import AuthenticationInteractor
from app.common.interactors.hack.auth_interactor import HackAuthenticationInteractor


@pytest.mark.parametrize(
    "first_name, last_name, uuid, password, role",
    [
        ("John", "Doe", uuid4(), "StrongPass123!", RoleEnum.ADMIN),
        ("Jane", "Doe", uuid4(), "StrongPass123!", RoleEnum.ORG_ADMIN),
        ("Hugo", "Bonnell", uuid4(), "StrongPass123!", RoleEnum.MEMBER),
        ],
    )
def test_admin_authentication(first_name: str, last_name: str, uuid: UUID, password: str, role: RoleEnum):
    try:
        # First create an admin and get his token
        admin_email = f"{uuid4()}@example.com"
        _ = HackAuthenticationInteractor.create_an_admin("Admin", "Admin", admin_email, "admin")
        admin_login_response = AdminAuthenticationInteractor.login(admin_email, "admin")

        assert admin_login_response.status_code == 200
        response_dict: dict = admin_login_response.json()
        admin_token = str(response_dict.get("access_token"))
        assert len(admin_token) > 0

        email = f"{uuid}@example.com"

        # Create an organization for users
        organization = HackAuthenticationInteractor.create_an_organization(name="AdminOrg")
        org_id = organization.id

        # Create users
        response = AdminAuthenticationInteractor.create_user(
            admin_token, first_name, last_name, email, password, role, org_id
        )
        assert response.status_code == 200

        user = UserModel(**response.json())
        assert user.first_name == first_name
        assert user.last_name == last_name
        assert user.email == email
        assert user.role == role
        assert user.credits == 0
        assert user.organization_id == org_id


        response_409 = AdminAuthenticationInteractor.create_user(
            admin_token, first_name, last_name, email, password, role, org_id
        )
        assert response_409.status_code == 409
        assert response_409.json().get("detail", "") == "Email already registered"

        response_401 = AdminAuthenticationInteractor.create_user(
            "wrong_tkn", first_name, last_name, email, password, role, org_id
        )
        assert response_401.status_code == 401
        assert response_401.json().get("detail", "") == "Invalid JWT token"

        response_404 = AdminAuthenticationInteractor.create_user(
            admin_token, first_name, last_name, "random_email", password, role, uuid4()
        )
        assert response_404.status_code == 404
        assert response_404.json().get("detail", "") == "Organization not found"

        if user.role != RoleEnum.ADMIN:
            response_400 = AdminAuthenticationInteractor.create_user(
                admin_token, first_name, last_name, "random_email", password, role, None
            )
            assert response_400.status_code == 400
            assert response_400.json().get("detail", "") == "User must have an organization_id"

        # Login
        response = AuthenticationInteractor.login(email, password)
        assert response.status_code == 200
        response_dict: dict = response.json()
        token = str(response_dict.get("access_token"))
        assert len(token) > 0


        # Test accessing admin EP as user
        if role != RoleEnum.ADMIN:
            response_403 = AdminAuthenticationInteractor.create_user(
                token, first_name, last_name, f"{uuid4()}@example.com", password, role, org_id
            )
            assert response_403.status_code == 403
            assert response_403.json().get("detail", "") == "User is not admin."


        for e, p in zip([email, "wrong_email", "wrong_email"], ["wrong_password", password, "wrong_password"]):
            response = AuthenticationInteractor.login(e, p)
            assert response.status_code == 401
            assert response.json().get("detail", "") == "Invalid email or password"

        # VerifyJWT
        for t, sc in zip([token, "invalid_token", None], [200, 401, 403]):
            response = AuthenticationInteractor.verifyjwt(t)
            assert response.status_code == sc
            if response.status_code == 401:
                assert response.json().get("detail") == "Invalid JWT token"
    finally:
        # Cleanup
        HackAuthenticationInteractor.delete_using_email(email)
        response = AuthenticationInteractor.login(email, password)
        assert response.status_code == 401

        HackAuthenticationInteractor.delete_using_email(admin_email)
        response = HackAuthenticationInteractor.login(admin_email, "admin")
        assert response.status_code == 401

        HackAuthenticationInteractor.delete_an_org_by_id(org_id)
        response = HackAuthenticationInteractor.get_org_by_id(org_id)
        assert response is None
