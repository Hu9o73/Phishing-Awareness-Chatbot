from uuid import uuid4

import pytest
from app.common.base_models import UserModel
from app.common.enum_models import RoleEnum
from app.common.interactors.admin.auth_interactor import AdminAuthenticationInteractor
from app.common.interactors.hack.auth_interactor import HackAuthenticationInteractor
from app.common.utils import clean_test, init_test


@pytest.mark.parametrize(
    "token_attr, expected_status, role, org, duplicate",
    [
        ("admin_token", 200, RoleEnum.MEMBER, "yes", False),
        ("admin_token", 200, RoleEnum.ORG_ADMIN, "yes", False),
        ("admin_token", 200, RoleEnum.ADMIN, "yes", False),
        ("admin_token", 200, RoleEnum.ADMIN, "yes", False),
        ("user_token", 403, RoleEnum.MEMBER, "yes", False),
        ("orgadmin_token", 403, RoleEnum.MEMBER, "yes", False),
        ("wrong_token", 401, RoleEnum.MEMBER, "yes", False),
        (None, 401, RoleEnum.MEMBER, "yes", False),
        ("admin_token", 400, RoleEnum.MEMBER, "no", False),
        ("admin_token", 400, RoleEnum.ORG_ADMIN, "no", False),
        ("admin_token", 404, RoleEnum.MEMBER, "wrong_id", False),
        ("admin_token", 404, RoleEnum.ORG_ADMIN, "wrong_id", False),
        ("admin_token", 409, RoleEnum.MEMBER, "yes", True),
    ],
    ids=[
        "create_member",
        "create_orgadmin",
        "create_admin_with_org",
        "create_admin_no_org",
        "member_forbbiden",
        "orgadmin_forbidden",
        "wrong_token",
        "no_token",
        "member_no_org",
        "orgadmin_no_org",
        "member_wrong_org_id",
        "orgadmin_wrong_org_id",
        "duplicate"
    ],
)
def test_admin_create_user(token_attr, expected_status, role, org, duplicate):
    env = init_test()
    user_id = None
    org_id = None
    if org == "yes":
        org_id = env.org.id
    elif org == "wrong_id":
        org_id = uuid4()

    try:
        token = getattr(env, token_attr) if token_attr and hasattr(env, token_attr) else token_attr

        custom_uuid = uuid4()
        email = f"{custom_uuid}@example.com" if not duplicate else env.user.email

        response = AdminAuthenticationInteractor.create_user(
            token, str(custom_uuid), str(custom_uuid), email, "pass", role, org_id
        )
        assert response.status_code == expected_status
        if response.status_code == 200:
            user = UserModel(**response.json())
            user_id = user.id
            assert user.email == email
            assert user.organization_id == org_id
            assert user.role == role
            assert user.first_name == str(custom_uuid)
            assert user.last_name == str(custom_uuid)

    finally:
        clean_test(env)
        if user_id:
            HackAuthenticationInteractor.delete_a_user_by_id(user_id)


@pytest.mark.parametrize(
    "token_attr,expected_status,user_id_type",
    [
        ("admin_token", 200, "accurate"),
        ("wrong_token", 401, "accurate"),
        (None, 401, "accurate"),
        ("user_token", 403, "accurate"),
        ("orgadmin_token", 403, "accurate"),
        ("admin_token", 200, "random"),
    ],
    ids=[
        "admin_ok",
        "wrong_token",
        "missing_token",
        "user_forbidden",
        "orgadmin_forbidden",
        "admin_nonexistent_user",
    ],
)
def test_admin_delete_user(token_attr, expected_status, user_id_type):
    env = init_test()
    custom_user = HackAuthenticationInteractor.create_a_user(
        str(uuid4()), str(uuid4()), f"{uuid4()}@user.com", "pass", env.org.id
    )

    try:
        token = getattr(env, token_attr) if token_attr and hasattr(env, token_attr) else token_attr
        user_id = custom_user.id if user_id_type == "accurate" else uuid4()

        response = AdminAuthenticationInteractor.delete_user(token, user_id)
        assert response.status_code == expected_status
    finally:
        clean_test(env)
        HackAuthenticationInteractor.delete_a_user_by_id(custom_user.id)


@pytest.mark.parametrize(
    "token_attr, expected_status, org",
    [
        ("admin_token", 200, True),
        ("wrong_token", 401, True),
        (None, 401, True),
        ("user_token", 403, True),
        ("orgadmin_token", 403, True),
        ("admin_token", 404, False),
    ],
    ids=[
        "admin_token",
        "wrong_token",
        "no_token",
        "user_token",
        "orgadmin_token",
        "wrong_org_id",
    ]
)
def test_admin_list_orgadmins(token_attr, expected_status, org):
    env = init_test()
    org_id = getattr(getattr(env, "org"), "id") if org else uuid4()
    try:
        token = getattr(env, token_attr) if token_attr and hasattr(env, token_attr) else token_attr
        response = AdminAuthenticationInteractor.list_orgadmins(token, org_id)
        assert response.status_code == expected_status
        if response.status_code == 200:
            assert len(response.json()) > 0
    finally:
        clean_test(env)
