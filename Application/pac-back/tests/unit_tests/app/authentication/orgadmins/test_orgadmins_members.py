from uuid import uuid4

import pytest
from app.common.base_models import OrgMemberModel
from app.common.interactors.hack.auth_interactor import HackAuthenticationInteractor
from app.common.interactors.orgadmin.auth_interactor import OrgAdminAuthenticationInteractor
from app.common.utils import clean_test, init_test


@pytest.mark.parametrize(
    "token_attr,expected_status",
    [
        ("orgadmin_token", 200),
        ("admin_token", 403),
        ("user_token", 403),
        (None, 401),
        ("wrong_token", 401),
    ],
    ids=[
        "orgadmin_ok",
        "admin_forbidden",
        "user_forbidden",
        "no_auth_invalid",
        "wrong_auth_invalid"
    ],
)
def test_orgadmin_create_member(token_attr, expected_status):
    env = init_test()
    member_id = None

    try:
        token = getattr(env, token_attr) if token_attr and hasattr(env, token_attr) else None

        custom_uuid = uuid4()
        email = f"{custom_uuid}@member.com"

        response = OrgAdminAuthenticationInteractor.create_member(
            token, str(custom_uuid), str(custom_uuid), email, env.org.id
        )
        assert response.status_code == expected_status

        if response.status_code == 200:
            member = OrgMemberModel(**response.json())
            member_id = member.id
            assert member.email == email
            assert member.organization_id == env.org.id
            assert member.first_name == str(custom_uuid)
            assert member.last_name == str(custom_uuid)

    finally:
        if member_id:
            HackAuthenticationInteractor.delete_a_member_by_id(member_id)
        clean_test(env)


@pytest.mark.parametrize(
    "token_attr,expected_status,member_type",
    [
        ("orgadmin_token", 200, "valid"),
        ("admin_token", 403, "valid"),
        ("user_token", 403, "valid"),
        (None, 401, "valid"),
        ("wrong_token", 401, "valid"),
        ("orgadmin_token", 404, "nonexistent"),
    ],
    ids=[
        "orgadmin_ok",
        "admin_forbidden",
        "user_forbidden",
        "no_auth_invalid",
        "wrong_auth_invalid",
        "nonexistent_member",
    ],
)
def test_orgadmin_get_member_by_id(token_attr, expected_status, member_type):
    env = init_test()
    member_id = None

    try:
        token = getattr(env, token_attr) if token_attr and hasattr(env, token_attr) else None

        if member_type == "valid":
            # Create a test member
            test_member = HackAuthenticationInteractor.create_an_org_member(
                str(uuid4()), str(uuid4()), f"{uuid4()}@member.com", str(env.org.id)
            )
            member_id = test_member.id
        else:
            member_id = uuid4()

        response = OrgAdminAuthenticationInteractor.get_member_by_id(token, member_id)
        assert response.status_code == expected_status

        if response.status_code == 200:
            member = OrgMemberModel(**response.json())
            assert member.id == member_id
            assert member.organization_id == env.org.id

    finally:
        clean_test(env)
        if member_id:
            HackAuthenticationInteractor.delete_a_member_by_id(member_id)


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
def test_orgadmin_get_members_in_organization(token_attr, expected_status):
    env = init_test()
    member_id = None

    try:
        token = getattr(env, token_attr) if token_attr and hasattr(env, token_attr) else token_attr

        # Create a test member to ensure list is not empty
        test_member = HackAuthenticationInteractor.create_an_org_member(
            str(uuid4()), str(uuid4()), f"{uuid4()}@member.com", str(env.org.id)
        )
        member_id = test_member.id

        response = OrgAdminAuthenticationInteractor.get_members_in_org(token)
        assert response.status_code == expected_status

        if response.status_code == 200:
            members = [OrgMemberModel(**member) for member in response.json()]
            assert isinstance(members, list)
            assert len(members) >= 1

            # Verify the test member is in the list
            member_ids = [member.id for member in members]
            assert member_id in member_ids

    finally:
        clean_test(env)
        if member_id:
            HackAuthenticationInteractor.delete_a_member_by_id(member_id)


@pytest.mark.parametrize(
    "token_attr,expected_status,member_type",
    [
        ("orgadmin_token", 200, "valid"),
        ("admin_token", 403, "valid"),
        ("user_token", 403, "valid"),
        (None, 401, "valid"),
        ("wrong_token", 401, "valid"),
        ("orgadmin_token", 404, "nonexistent"),
    ],
    ids=[
        "orgadmin_ok",
        "admin_forbidden",
        "user_forbidden",
        "no_auth_invalid",
        "wrong_auth_invalid",
        "nonexistent_member",
    ],
)
def test_orgadmin_delete_member(token_attr, expected_status, member_type):
    env = init_test()
    member_id = None

    try:
        token = getattr(env, token_attr) if token_attr and hasattr(env, token_attr) else None

        if member_type == "valid":
            test_member = HackAuthenticationInteractor.create_an_org_member(
                str(uuid4()), str(uuid4()), f"{uuid4()}@member.com", str(env.org.id)
            )
            delete_id = test_member.id
        else:
            delete_id = uuid4()

        response = OrgAdminAuthenticationInteractor.delete_member_by_id(token, delete_id)
        assert response.status_code == expected_status

        if response.status_code == 200:
            assert response.json().get("status") == "ok"

    finally:
        clean_test(env)
        if member_id:
            HackAuthenticationInteractor.delete_a_member_by_id(member_id)
