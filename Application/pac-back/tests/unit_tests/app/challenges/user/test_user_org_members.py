from __future__ import annotations

from uuid import uuid4

import pytest
from app.common.interactors.hack.auth_interactor import HackAuthenticationInteractor
from app.common.interactors.user.challenges_interactor import UserChallengesInteractor
from app.common.utils import clean_test, init_test

pytestmark = pytest.mark.e2e


def _resolve_token(env, token_attr: str | None) -> str | None:
    if token_attr is None:
        return None
    if token_attr == "wrong_token":
        return "wrong_token"
    return getattr(env, token_attr)


def _create_member(env, member_ids: set):
    member = HackAuthenticationInteractor.create_an_org_member(
        first_name=str(uuid4()),
        last_name=str(uuid4()),
        email=f"{uuid4()}@members.test",
        org_id=env.org.id,
    )
    member_ids.add(member.id)
    return member


@pytest.fixture
def test_env():
    env = init_test()
    member_ids: set = set()
    extra_org_ids: set = set()
    try:
        yield env, member_ids, extra_org_ids
    finally:
        for org_id in list(extra_org_ids):
            HackAuthenticationInteractor.delete_an_org_by_id(org_id)
        clean_test(env)


@pytest.mark.parametrize(
    "token_attr,expected_status,expect_item",
    [
        ("user_token", 200, True),
        ("orgadmin_token", 403, False),
        ("admin_token", 403, False),
        ("wrong_token", 502, False),
        (None, 403, False),
    ],
    ids=[
        "user",
        "orgadmin_forbidden",
        "admin_forbidden",
        "invalid_token",
        "missing_token",
    ],
)
def test_list_org_members_authorization(test_env, token_attr, expected_status, expect_item):
    env, member_ids, _ = test_env
    member = _create_member(env, member_ids) if expect_item else None

    token = _resolve_token(env, token_attr)
    response = UserChallengesInteractor.list_org_members(token)

    assert response.status_code == expected_status
    if expected_status == 200 and member is not None:
        payload = response.json()
        ids = [item["id"] for item in payload]
        assert str(member.id) in ids


def test_list_org_members_filters_by_id(test_env):
    env, member_ids, _ = test_env
    member = _create_member(env, member_ids)

    response = UserChallengesInteractor.list_org_members(env.user_token, str(member.id))

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
    assert payload[0]["id"] == str(member.id)


def test_list_org_members_rejects_foreign_member(test_env):
    env, member_ids, extra_org_ids = test_env
    foreign_org = HackAuthenticationInteractor.create_an_organization(str(uuid4()))
    extra_org_ids.add(foreign_org.id)
    foreign_member = HackAuthenticationInteractor.create_an_org_member(
        first_name=str(uuid4()),
        last_name=str(uuid4()),
        email=f"{uuid4()}@foreign.test",
        org_id=foreign_org.id,
    )

    response = UserChallengesInteractor.list_org_members(env.user_token, str(foreign_member.id))

    assert response.status_code == 404
    assert response.json().get("detail")
