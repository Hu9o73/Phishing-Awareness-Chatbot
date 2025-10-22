from uuid import uuid4

import pytest
from app.common.base_models import PublicUserModel, UserModel
from app.common.interactors.hack.auth_interactor import HackAuthenticationInteractor
from app.common.interactors.orgadmin.auth_interactor import OrgAdminAuthenticationInteractor
from app.common.utils import clean_test, init_test


@pytest.mark.parametrize(
    "token_attr,expected_status,duplicate",
    [
        ("orgadmin_token", 200, False),
        ("wrong_token", 401, False),
        (None, 401, False),
        ("user_token", 403, False),
        ("admin_token", 403, False),
        ("orgadmin_token", 409, True),
    ],
    ids=[
        "orgadmin_ok",
        "wrong_token",
        "missing_token",
        "user_forbidden",
        "admin_not_orgadmin",
        "duplicate_email",
    ],
)
def test_orgadmin_create_user(token_attr, expected_status, duplicate):
    env = init_test()
    user_id = None

    try:
        token = getattr(env, token_attr) if token_attr and hasattr(env, token_attr) else token_attr

        custom_uuid = uuid4()
        email = f"{custom_uuid}@example.com" if not duplicate else env.user.email

        response = OrgAdminAuthenticationInteractor.create_user(
            token, str(custom_uuid), str(custom_uuid), email, "pass"
        )
        assert response.status_code == expected_status

        if response.status_code == 200:
            user = UserModel(**response.json())
            user_id = user.id
            assert user.email == email
            assert user.organization_id == env.org.id
            assert user.first_name == str(custom_uuid)
            assert user.last_name == str(custom_uuid)

    finally:
        if user_id:
            HackAuthenticationInteractor.delete_a_user_by_id(user_id)
        clean_test(env)


@pytest.mark.parametrize(
    "token_attr,expected_status",
    [
        ("orgadmin_token", 200),
        ("wrong_token", 401),
        (None, 401),
        ("user_token", 403),
        ("admin_token", 403),
    ],
    ids=[
        "orgadmin_ok",
        "wrong_token",
        "missing_token",
        "user_forbidden",
        "admin_forbidden",
    ],
)
def test_orgadmin_list_users(token_attr, expected_status):
    env = init_test()

    try:
        token = getattr(env, token_attr) if token_attr and hasattr(env, token_attr) else token_attr

        response = OrgAdminAuthenticationInteractor.list_users(token)
        assert response.status_code == expected_status

        if response.status_code == 200:
            users = [PublicUserModel(**user) for user in response.json()]

            user_emails = [user.email for user in users]
            assert env.user.email in user_emails
            assert env.orgadmin.email not in user_emails

    finally:
        clean_test(env)


@pytest.mark.parametrize(
    "token_attr,expected_status,user_type",
    [
        ("orgadmin_token", 200, "valid"),
        ("wrong_token", 401, "valid"),
        (None, 401, "valid"),
        ("user_token", 403, "valid"),
        ("admin_token", 403, "valid"),
        ("orgadmin_token", 404, "nonexistent"),
        ("orgadmin_token", 404, "other_org"),
    ],
    ids=[
        "orgadmin_ok",
        "wrong_token",
        "missing_token",
        "user_forbidden",
        "admin_not_orgadmin",
        "nonexistent_user",
        "user_from_other_org",
    ],
)
def test_orgadmin_delete_user(token_attr, expected_status, user_type):
    env = init_test()
    test_user_id = None
    other_org_id = None

    try:
        token = getattr(env, token_attr) if token_attr and hasattr(env, token_attr) else token_attr

        if user_type == "valid":
            user_id = env.user.id
        elif user_type == "nonexistent":
            user_id = uuid4()
        else:  # other_org
            # Create a user in a different organization
            other_org = HackAuthenticationInteractor.create_an_organization(str(uuid4()))
            other_org_id = other_org.id
            test_user = HackAuthenticationInteractor.create_a_user(
                str(uuid4()), str(uuid4()), f"{uuid4()}@test.com", "pass", other_org_id
            )
            user_id = test_user.id

        response = OrgAdminAuthenticationInteractor.delete_user(token, str(user_id))
        assert response.status_code == expected_status

        if response.status_code == 200:
            assert response.json().get("message") == f"Delete user with id {user_id}"

    finally:
        if test_user_id:
            HackAuthenticationInteractor.delete_a_user_by_id(test_user_id)
        if other_org_id:
            HackAuthenticationInteractor.delete_an_org_by_id(other_org_id)
        clean_test(env)
