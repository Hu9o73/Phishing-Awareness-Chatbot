from uuid import UUID, uuid4

import pytest
from app.common.base_models import MemberModel, PublicUserModel, UserModel
from app.common.enum_models import RoleEnum
from app.common.interactors.admin.auth_interactor import AdminAuthenticationInteractor
from app.common.interactors.base.auth_interactor import AuthenticationInteractor
from app.common.interactors.hack.auth_interactor import HackAuthenticationInteractor
from app.common.interactors.orgadmin.auth_interactor import OrgAdminAuthenticationInteractor


def test_get_current_user():
    admin_email = f"{uuid4()}@example.com"
    try:
        _ = HackAuthenticationInteractor.create_an_admin("Admin", "Admin", admin_email, "admin")
        admin_login_response = AdminAuthenticationInteractor.login(admin_email, "admin")

        assert admin_login_response.status_code == 200
        response_dict: dict = admin_login_response.json()
        token = str(response_dict.get("access_token"))
        assert len(token) > 0

        response = AuthenticationInteractor.get_current_user(token)
        assert response.status_code == 200
        user = PublicUserModel(**response.json())
        assert user.email == admin_email
        assert user.first_name == "Admin"
        assert user.last_name == "Admin"
        user_id = user.id

        HackAuthenticationInteractor.delete_using_email(admin_email)
        response_404 = AuthenticationInteractor.get_current_user(token)
        assert response_404.status_code == 404
        assert response_404.json().get("detail", "") == f"User with id {user_id} not found"

        for t, sc in zip(["wrong_token", None], [401, 403]):
            response = AuthenticationInteractor.get_current_user(t)
            assert response.status_code == sc

    finally:
        # Cleanup
        HackAuthenticationInteractor.delete_using_email(admin_email)
        response = AuthenticationInteractor.login(admin_email, "admin")
        assert response.status_code == 401


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


@pytest.mark.parametrize(
    "first_name, last_name, uuid, password",
    [
        ("John", "ZeOrgAdmin", uuid4(), "StrongPass123!"),
    ],
)
def test_orgadmin_authentication(first_name: str, last_name: str, uuid: UUID, password: str):
    try:
        # Create an organization for users
        organization = HackAuthenticationInteractor.create_an_organization(name="AdminOrg2")
        org_id = organization.id

        # Create an org admin and get his token
        email = f"{uuid}@example.com"
        _ = HackAuthenticationInteractor.create_an_org_admin(first_name, last_name, email, password, org_id)
        orgadmin_login_response = AuthenticationInteractor.login(email, password)

        assert orgadmin_login_response.status_code == 200
        response_dict: dict = orgadmin_login_response.json()
        orgadmin_token = str(response_dict.get("access_token"))
        assert len(orgadmin_token) > 0

        # Try to list the users when no users
        response = OrgAdminAuthenticationInteractor.list_users(orgadmin_token)
        assert response.status_code == 200
        users_listed = [PublicUserModel(**user) for user in response.json()]
        assert len(users_listed) == 0

        # Create users
        response = OrgAdminAuthenticationInteractor.create_user(
            orgadmin_token, "Test", "USER", "test@user.com", "userpass"
        )
        assert response.status_code == 200

        user = UserModel(**response.json())
        assert user.first_name == "Test"
        assert user.last_name == "USER"
        assert user.email == "test@user.com"
        assert user.role == RoleEnum.MEMBER
        assert user.credits == 0
        assert user.organization_id == org_id

        # Create a second user
        response = OrgAdminAuthenticationInteractor.create_user(
            orgadmin_token, "Test2", "USER2", "test2@user.com", "userpass"
        )
        assert response.status_code == 200
        user = UserModel(**response.json())
        user_id = user.id

        response_409 = OrgAdminAuthenticationInteractor.create_user(
            orgadmin_token, "Test", "USER", "test@user.com", "userpass"
        )
        assert response_409.status_code == 409
        assert response_409.json().get("detail", "") == "Email already registered"

        response_401 = OrgAdminAuthenticationInteractor.create_user(
            "wrongtoken", "Test", "USER", "test@user.com", "userpass"
        )
        assert response_401.status_code == 401
        assert response_401.json().get("detail", "") == "Invalid JWT token"

        # Try to list the users
        response = OrgAdminAuthenticationInteractor.list_users(orgadmin_token)
        assert response.status_code == 200
        users_listed = [PublicUserModel(**user) for user in response.json()]
        assert len(users_listed) == 2

        # Try to delete a user
        response = OrgAdminAuthenticationInteractor.delete_user(orgadmin_token, user_id)
        assert response.status_code == 200
        assert response.json().get("message", "") == f"Delete user with id {user_id}"

        # List again, with one user left
        response = OrgAdminAuthenticationInteractor.list_users(orgadmin_token)
        assert response.status_code == 200
        users_listed = [PublicUserModel(**user) for user in response.json()]
        assert len(users_listed) == 1

        # Try to delete with wrong user_id
        my_wrong_uuid = uuid4()
        response_404 = OrgAdminAuthenticationInteractor.delete_user(orgadmin_token, my_wrong_uuid)
        assert response_404.status_code == 404
        assert response_404.json().get("detail", "") == f"User with id {my_wrong_uuid} not found."

        # Login
        response = AuthenticationInteractor.login("test@user.com", "userpass")
        assert response.status_code == 200
        response_dict: dict = response.json()
        user_token = str(response_dict.get("access_token"))
        assert len(user_token) > 0


        # Test accessing admin EP as a user
        response_403 = OrgAdminAuthenticationInteractor.create_user(
            user_token, first_name, last_name, f"{uuid4()}@example.com", password
        )
        assert response_403.status_code == 403
        assert response_403.json().get("detail", "") == "User is not admin of his organization."

        response_403 = OrgAdminAuthenticationInteractor.list_users(user_token)
        assert response_403.status_code == 403
        assert response_403.json().get("detail", "") == "User is not admin of his organization."

        response_403 = OrgAdminAuthenticationInteractor.delete_user(user_token, uuid4())
        assert response_403.status_code == 403
        assert response_403.json().get("detail", "") == "User is not admin of his organization."

    finally:
        # Cleanup
        HackAuthenticationInteractor.delete_using_email(email)
        response = AuthenticationInteractor.login(email, password)
        assert response.status_code == 401

        HackAuthenticationInteractor.delete_using_email("test@user.com")
        response = HackAuthenticationInteractor.login("test@user.com", "userpass")
        assert response.status_code == 401

        HackAuthenticationInteractor.delete_using_email("test2@user.com")
        response = HackAuthenticationInteractor.login("test2@user.com", "userpass")
        assert response.status_code == 401

        HackAuthenticationInteractor.delete_an_org_by_id(org_id)
        response = HackAuthenticationInteractor.get_org_by_id(org_id)
        assert response is None



def test_orgadmin_member_management():
    email = f"{uuid4()}@example.com"
    admin_email = f"{uuid4()}@example.com"
    user_email = f"{uuid4()}@example.com"
    try:
        # Create an organization for users
        organization = HackAuthenticationInteractor.create_an_organization(name="AdminOrg2")
        org_id = organization.id

        # Create an org admin and get his token
        password = "orgadminpass"
        _ = HackAuthenticationInteractor.create_an_org_admin("John", "THESECONDORGADMIN", email, password, org_id)
        orgadmin_login_response = AuthenticationInteractor.login(email, password)

        assert orgadmin_login_response.status_code == 200
        response_dict: dict = orgadmin_login_response.json()
        orgadmin_token = str(response_dict.get("access_token"))
        assert len(orgadmin_token) > 0

        # Create an admin and get its token
        _ = HackAuthenticationInteractor.create_an_admin("Test", "ADMIN", admin_email, "adminpass")
        admin_login_response = AuthenticationInteractor.login(admin_email, "adminpass")
        assert admin_login_response.status_code == 200
        response_dict: dict = admin_login_response.json()
        admin_token = str(response_dict.get("access_token"))
        assert len(admin_token) > 0

        # Create a user and get its token
        _ = AdminAuthenticationInteractor.create_user(
            admin_token, "Test", "USER", user_email, "userpass", RoleEnum.MEMBER, org_id
        )
        response = AuthenticationInteractor.login(user_email, "userpass")
        assert response.status_code == 200
        response_dict: dict = response.json()
        user_token = str(response_dict.get("access_token"))
        assert len(user_token) > 0


        # Create members
        members_ids = []
        for _ in range(10):
            response = OrgAdminAuthenticationInteractor.create_member(
                orgadmin_token, "Test", "MEMBER", f"{str(uuid4())}@example.com", org_id
            )
            assert response.status_code == 200
            member = MemberModel(**response.json())
            assert member.first_name == "Test"
            assert member.last_name == "MEMBER"
            assert member.organization_id == org_id
            members_ids.append(member.id)


        # Try to get member by id
        response = OrgAdminAuthenticationInteractor.get_member_by_id(orgadmin_token, members_ids[0])
        assert response.status_code == 200
        member = MemberModel(**response.json())
        assert member.id == members_ids[0]

        # Try to get member by id - Member not found
        random_uuid = uuid4()
        response_404 = OrgAdminAuthenticationInteractor.get_member_by_id(orgadmin_token, random_uuid)
        assert response_404.status_code == 404
        assert response_404.json().get("detail", "") == f"Member with id {random_uuid} not found"

        # Try to get member by id - Invalid token
        response_401 = OrgAdminAuthenticationInteractor.get_member_by_id("wrongtoken", members_ids[0])
        assert response_401.status_code == 401
        assert response_401.json().get("detail", "") == "Invalid JWT token"

        # Try to get member by id - Forbidden
        response_403 = OrgAdminAuthenticationInteractor.get_member_by_id(admin_token, members_ids[0])
        assert response_403.status_code == 403
        assert response_403.json().get("detail", "") == "User is not admin of his organization."

        # Try to get member by id - Forbidden
        response_403 = OrgAdminAuthenticationInteractor.get_member_by_id(user_token, members_ids[0])
        assert response_403.status_code == 403
        assert response_403.json().get("detail", "") == "User is not admin of his organization."


        # Delete member
        response = OrgAdminAuthenticationInteractor.delete_member_by_id(orgadmin_token, members_ids[1])
        assert response.status_code == 200
        assert response.json().get("message", "") == f"Member {members_ids[1]} deleted succesfully"

        # Try to get member by id - Invalid token
        response_401 = OrgAdminAuthenticationInteractor.delete_member_by_id("wrongtoken", members_ids[1])
        assert response_401.status_code == 401
        assert response_401.json().get("detail", "") == "Invalid JWT token"

        # Try to get member by id - Forbidden
        response_403 = OrgAdminAuthenticationInteractor.delete_member_by_id(admin_token, members_ids[1])
        assert response_403.status_code == 403
        assert response_403.json().get("detail", "") == "User is not admin of his organization."

        # Try to get member by id - Forbidden
        response_403 = OrgAdminAuthenticationInteractor.delete_member_by_id(user_token, members_ids[1])
        assert response_403.status_code == 403
        assert response_403.json().get("detail", "") == "User is not admin of his organization."


        # List members
        response = OrgAdminAuthenticationInteractor.get_members_in_org(orgadmin_token)
        assert response.status_code == 200
        members = [MemberModel(**member) for member in response.json()]
        assert len(members) == 9
        assert members[0].id == members_ids[0]
        assert members[0].organization_id == org_id

    finally:
        # Cleanup
        HackAuthenticationInteractor.delete_using_email(email)
        response = AuthenticationInteractor.login(email, password)
        assert response.status_code == 401

        HackAuthenticationInteractor.delete_using_email(user_email)
        response = HackAuthenticationInteractor.login(user_email, "userpass")
        assert response.status_code == 401

        HackAuthenticationInteractor.delete_using_email(admin_email)
        response = HackAuthenticationInteractor.login(admin_email, "adminpass")
        assert response.status_code == 401

        HackAuthenticationInteractor.delete_an_org_by_id(org_id)
        response = HackAuthenticationInteractor.get_org_by_id(org_id)
        assert response is None
