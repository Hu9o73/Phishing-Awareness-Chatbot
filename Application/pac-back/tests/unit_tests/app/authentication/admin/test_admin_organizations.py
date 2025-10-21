from uuid import uuid4

import pytest
from app.common.base_models import OrganizationModel
from app.common.interactors.admin.auth_interactor import AdminAuthenticationInteractor
from app.common.interactors.hack.auth_interactor import HackAuthenticationInteractor
from app.common.utils import clean_test, init_test


@pytest.mark.parametrize(
    "token_attr,expected_status,org_description",
    [
        ("admin_token", 200, "Test Description"),
        ("admin_token", 200, None),
        ("wrong_token", 401, "Test Description"),
        (None, 401, "Test Description"),
        ("user_token", 403, "Test Description"),
        ("orgadmin_token", 403, "Test Description"),
    ],
    ids=[
        "admin_ok_with_description",
        "admin_ok_no_description",
        "wrong_token",
        "missing_token",
        "user_forbidden",
        "orgadmin_forbidden",
    ],
)
def test_admin_create_organization(token_attr, expected_status, org_description):
    env = init_test()
    created_org_id = None
    org_name = str(uuid4())

    try:
        token = getattr(env, token_attr) if token_attr and hasattr(env, token_attr) else token_attr

        response = AdminAuthenticationInteractor.create_org(token, org_name, org_description)
        assert response.status_code == expected_status

        if response.status_code == 200:
            org = OrganizationModel(**response.json())
            created_org_id = org.id
            assert org.name == org_name
            if org_description:
                assert org.description == org_description

    finally:
        clean_test(env)
        if created_org_id:
            HackAuthenticationInteractor.delete_an_org_by_id(created_org_id)


@pytest.mark.parametrize(
    "token_attr,expected_status",
    [
        ("admin_token", 200),
        ("wrong_token", 401),
        (None, 401),
        ("user_token", 403),
        ("orgadmin_token", 403),
    ],
    ids=[
        "admin_ok",
        "wrong_token",
        "missing_token",
        "user_forbidden",
        "orgadmin_forbidden",
    ],
)
def test_admin_list_organizations(token_attr, expected_status):
    env = init_test()

    try:
        token = getattr(env, token_attr) if token_attr and hasattr(env, token_attr) else token_attr

        response = AdminAuthenticationInteractor.list_all_orgs(token)
        assert response.status_code == expected_status

        if response.status_code == 200:
            orgs = response.json()
            assert isinstance(orgs, list)
            assert len(orgs) >= 1

            org_ids = [org["id"] for org in orgs]
            assert str(env.org.id) in org_ids

    finally:
        clean_test(env)


@pytest.mark.parametrize(
    "token_attr,expected_status,org_type",
    [
        ("admin_token", 200, "valid"),
        ("wrong_token", 401, "valid"),
        (None, 401, "valid"),
        ("user_token", 403, "valid"),
        ("orgadmin_token", 403, "valid"),
        ("admin_token", 404, "nonexistent"),
    ],
    ids=[
        "admin_ok",
        "wrong_token",
        "missing_token",
        "user_forbidden",
        "orgadmin_forbidden",
        "nonexistent_org",
    ],
)
def test_admin_delete_organization(token_attr, expected_status, org_type):
    env = init_test()

    try:
        token = getattr(env, token_attr) if token_attr and hasattr(env, token_attr) else token_attr

        if org_type == "valid":
            org_id = env.org.id
        else:
            org_id = uuid4()

        response = AdminAuthenticationInteractor.delete_org(token, org_id)
        assert response.status_code == expected_status

        if response.status_code == 200:
            assert response.json().get("status") == "ok"

    finally:
        clean_test(env)
