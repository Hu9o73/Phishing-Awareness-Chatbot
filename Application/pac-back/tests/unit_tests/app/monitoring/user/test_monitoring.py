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


def _hook_email_payload() -> dict:
    suffix = str(uuid4())
    return {
        "subject": f"Hook subject {suffix}",
        "sender_email": f"hook-{suffix[:8]}@monitoring.test",
        "language": "en",
        "body": f"Hook body {suffix}",
        "variables": {"seed": suffix},
    }


def _create_scenario(env, scenario_ids: set[str], email_ids: set[str]) -> UUID:
    payload = _scenario_payload()
    response = UserChallengesInteractor.create_scenario(env.user_token, payload)
    assert response.status_code == 201
    scenario_id = response.json()["id"]
    scenario_ids.add(scenario_id)

    hook_response = UserChallengesInteractor.create_hook_email(env.user_token, scenario_id, _hook_email_payload())
    assert hook_response.status_code == 201
    hook_email = hook_response.json()
    email_ids.add(hook_email["id"])
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
    scenario_id = _create_scenario(env, scenario_ids, email_ids)
    member = _create_member(env, member_ids)

    response = UserMonitoringInteractor.start_challenge(env.user_token, member.id, scenario_id)
    assert response.status_code == 201
    data = response.json()
    challenge_ids.add(data["id"])
    if data.get("last_exchange_id"):
        email_ids.add(data["last_exchange_id"])
    assert data["user_id"] == str(env.user.id)
    return data


def _create_follow_up_email(scenario_id: str, previous_email_id: str, email_ids: set[str], role: str = "USER") -> str:
    supabase = get_db()
    payload = {
        "scenario_id": scenario_id,
        "role": role,
        "target_id": None,
        "previous_email": previous_email_id,
        "subject": f"Follow up {uuid4()}",
        "sender_email": f"{role.lower()}-{uuid4()}@monitoring.test",
        "language": "en",
        "body": "Test follow up",
        "variables": {"source": "unit-test"},
    }
    response = supabase.table("emails").insert(payload).execute()
    assert response.data
    email_id = response.data[0]["id"]
    email_ids.add(email_id)
    return email_id


def _update_challenge_last_exchange(challenge_id: str, exchange_id: str):
    supabase = get_db()
    response = (
        supabase.table("challenges")
        .update({"last_exchange_id": exchange_id})
        .eq("id", challenge_id)
        .execute()
    )
    assert response.data


def _update_challenge_status(challenge_id: str, status: str):
    supabase = get_db()
    response = supabase.table("challenges").update({"status": status}).eq("id", challenge_id).execute()
    assert response.data


def _insert_challenge_record(user_id: UUID, employee_id: UUID, scenario_id: str, challenge_ids: set[str], status: str):
    supabase = get_db()
    payload = {
        "user_id": str(user_id),
        "employee_id": str(employee_id),
        "scenario_id": scenario_id,
        "channel": "EMAIL",
        "status": status,
        "score": None,
        "last_exchange_id": None,
    }
    response = supabase.table("challenges").insert(payload).execute()
    assert response.data
    challenge_id = response.data[0]["id"]
    challenge_ids.add(challenge_id)
    return challenge_id


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
    scenario_id = _create_scenario(env, scenario_ids, email_ids)
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
def test_list_challenges_authorization(test_env, token_attr, expected_status, expect_item):
    env, scenario_ids, member_ids, challenge_ids, email_ids = test_env
    created_id = None
    if expect_item:
        challenge_data = _start_valid_challenge(env, scenario_ids, member_ids, challenge_ids, email_ids)
        created_id = challenge_data["id"]

    token = _resolve_token(env, token_attr)
    response = UserMonitoringInteractor.list_challenges(token)

    assert response.status_code == expected_status
    if expected_status == 200 and created_id:
        items = response.json().get("items", [])
        assert any(item["id"] == created_id for item in items)


def test_list_challenges_filters_only_user_ongoing(test_env):
    env, scenario_ids, member_ids, challenge_ids, email_ids = test_env
    challenge_data = _start_valid_challenge(env, scenario_ids, member_ids, challenge_ids, email_ids)

    closed_member = _create_member(env, member_ids)
    closed_challenge_id = _insert_challenge_record(
        env.user.id, closed_member.id, challenge_data["scenario_id"], challenge_ids, "ONGOING"
    )
    _update_challenge_status(closed_challenge_id, "SUCCESS")

    foreign_member = _create_member(env, member_ids)
    foreign_challenge_id = _insert_challenge_record(
        env.orgadmin.id, foreign_member.id, challenge_data["scenario_id"], challenge_ids, "ONGOING"
    )

    response = UserMonitoringInteractor.list_challenges(env.user_token, "ONGOING")

    assert response.status_code == 200
    items = response.json().get("items", [])
    returned_ids = [item["id"] for item in items]
    assert challenge_data["id"] in returned_ids
    assert closed_challenge_id not in returned_ids
    assert foreign_challenge_id not in returned_ids
    assert all(item["status"] == "ONGOING" for item in items)
    assert all(item["user_id"] == str(env.user.id) for item in items)


def test_list_challenges_returns_all_statuses_when_no_filter(test_env):
    env, scenario_ids, member_ids, challenge_ids, email_ids = test_env
    ongoing_challenge = _start_valid_challenge(env, scenario_ids, member_ids, challenge_ids, email_ids)

    member = _create_member(env, member_ids)
    success_challenge = _insert_challenge_record(
        env.user.id, member.id, ongoing_challenge["scenario_id"], challenge_ids, "SUCCESS"
    )

    response = UserMonitoringInteractor.list_challenges(env.user_token)

    assert response.status_code == 200
    items = response.json().get("items", [])
    returned_ids = [item["id"] for item in items]
    assert ongoing_challenge["id"] in returned_ids
    assert success_challenge in returned_ids
    assert all(item["user_id"] == str(env.user.id) for item in items)


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


def test_get_exchanges_follows_previous_chain(test_env):
    env, scenario_ids, member_ids, challenge_ids, email_ids = test_env
    challenge_data = _start_valid_challenge(env, scenario_ids, member_ids, challenge_ids, email_ids)

    hook_id = challenge_data["last_exchange_id"]
    assert hook_id is not None

    ai_email_id = _create_follow_up_email(challenge_data["scenario_id"], hook_id, email_ids, role="AI")
    user_email_id = _create_follow_up_email(challenge_data["scenario_id"], ai_email_id, email_ids, role="USER")
    _update_challenge_last_exchange(challenge_data["id"], user_email_id)

    response = UserMonitoringInteractor.get_exchanges(env.user_token, challenge_data["id"])

    assert response.status_code == 200
    exchanges = response.json().get("exchanges", [])
    assert len(exchanges) >= 3
    assert [exchange["id"] for exchange in exchanges[:3]] == [hook_id, ai_email_id, user_email_id]
    assert exchanges[0]["role"] == "HOOK"
    assert exchanges[1]["role"] == "AI"
    assert exchanges[2]["role"] == "USER"
