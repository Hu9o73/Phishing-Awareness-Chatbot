from __future__ import annotations

from uuid import UUID, uuid4

import pytest

from app.common.base_models import OrgMemberModel
from app.common.database.client import get_db
from app.common.interactors.hack.auth_interactor import HackAuthenticationInteractor
from app.common.interactors.user.challenges_interactor import UserChallengesInteractor
from app.common.interactors.user.monitoring_interactor import UserMonitoringInteractor
from app.common.utils import clean_test, init_test

pytestmark = pytest.mark.e2e


def _resolve_token(env, token_attr: str | None) -> str | None:
    if token_attr is None:
        return None
    if token_attr == "wrong_token":
        return "wrong_token"
    return getattr(env, token_attr)


def _scenario_payload() -> dict:
    suffix = str(uuid4())
    return {
        "name": f"Scenario {suffix}",
        "complexity": "EASY",
        "system_prompt": f"Prompt {suffix}",
        "misc_info": {"seed": suffix},
    }


def _create_scenario(env, scenario_ids: set[str]) -> UUID:
    payload = _scenario_payload()
    response = UserChallengesInteractor.create_scenario(env.user_token, payload)
    assert response.status_code == 201
    scenario_id = response.json()["id"]
    scenario_ids.add(scenario_id)
    return UUID(scenario_id)


def _create_member(env, member_ids: set[UUID]) -> OrgMemberModel:
    member = HackAuthenticationInteractor.create_an_org_member(
        first_name=str(uuid4()),
        last_name=str(uuid4()),
        email=f"{uuid4()}@monitoring.test",
        org_id=env.org.id,
    )
    member_ids.add(member.id)
    return member


def _cleanup_records(env, scenario_ids: set[str], member_ids: set[UUID], challenge_ids: set[str], email_ids: set[str]):
    supabase = get_db()
    for challenge_id in list(challenge_ids):
        supabase.table("challenges").delete().eq("id", challenge_id).execute()
    for email_id in list(email_ids):
        supabase.table("emails").delete().eq("id", email_id).execute()
    for scenario_id in list(scenario_ids):
        UserChallengesInteractor.delete_scenario(env.user_token, scenario_id)
    for member_id in list(member_ids):
        HackAuthenticationInteractor.delete_a_member_by_id(member_id)


def _start_valid_challenge(env, scenario_ids, member_ids, challenge_ids, email_ids):
    scenario_id = _create_scenario(env, scenario_ids)
    member = _create_member(env, member_ids)

    response = UserMonitoringInteractor.start_challenge(env.user_token, member.id, scenario_id)
    assert response.status_code == 201
    data = response.json()
    challenge_ids.add(data["id"])
    if data.get("last_exchange_id"):
        email_ids.add(data["last_exchange_id"])
    assert data["user_id"] == str(env.user.id)
    return data


@pytest.fixture
def test_env():
    env = init_test()
    scenario_ids: set[str] = set()
    member_ids: set[UUID] = set()
    challenge_ids: set[str] = set()
    email_ids: set[str] = set()
    try:
        yield env, scenario_ids, member_ids, challenge_ids, email_ids
    finally:
        _cleanup_records(env, scenario_ids, member_ids, challenge_ids, email_ids)
        clean_test(env)


@pytest.mark.parametrize(
    "token_attr,expected_status",
    [
        ("user_token", 201),
        ("orgadmin_token", 403),
        ("admin_token", 403),
        ("wrong_token", 502),
        (None, 403),
    ],
    ids=[
        "user",
        "orgadmin_forbidden",
        "admin_forbidden",
        "invalid_token",
        "missing_token",
    ],
)
def test_start_challenge_authorization(test_env, token_attr, expected_status):
    env, scenario_ids, member_ids, challenge_ids, email_ids = test_env
    scenario_id = _create_scenario(env, scenario_ids)
    member = _create_member(env, member_ids)

    token = _resolve_token(env, token_attr)
    response = UserMonitoringInteractor.start_challenge(token, member.id, scenario_id)

    assert response.status_code == expected_status
    if expected_status == 201:
        payload = response.json()
        challenge_ids.add(payload["id"])
        if payload.get("last_exchange_id"):
            email_ids.add(payload["last_exchange_id"])
        assert payload["user_id"] == str(env.user.id)
        assert payload["employee_id"] == str(member.id)
        assert payload["scenario_id"] == str(scenario_id)
        assert payload["channel"] == "EMAIL"
        assert payload["status"] == "ONGOING"


def test_retrieve_status_returns_challenge_status(test_env):
    env, scenario_ids, member_ids, challenge_ids, email_ids = test_env
    challenge_data = _start_valid_challenge(env, scenario_ids, member_ids, challenge_ids, email_ids)

    response = UserMonitoringInteractor.retrieve_status(env.user_token, challenge_data["id"])

    assert response.status_code == 200
    assert response.json()["status"] == "ONGOING"


def test_get_exchanges_returns_hook_first(test_env):
    env, scenario_ids, member_ids, challenge_ids, email_ids = test_env
    challenge_data = _start_valid_challenge(env, scenario_ids, member_ids, challenge_ids, email_ids)

    response = UserMonitoringInteractor.get_exchanges(env.user_token, challenge_data["id"])

    assert response.status_code == 200
    exchanges = response.json().get("exchanges", [])
    assert len(exchanges) >= 1
    assert exchanges[0]["role"] == "HOOK"
    if challenge_data.get("last_exchange_id"):
        assert exchanges[0]["id"] == challenge_data["last_exchange_id"]
