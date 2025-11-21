from __future__ import annotations

import json
from uuid import uuid4

import pytest
from app.common.interactors.user.challenges_interactor import UserChallengesInteractor
from app.common.utils import clean_test, init_test

pytestmark = pytest.mark.e2e


def _cleanup_scenarios(token: str | None, scenario_ids: set[str]):
    for scenario_id in list(scenario_ids):
        response = UserChallengesInteractor.delete_scenario(token, scenario_id)
        if response.status_code in (200, 404):
            scenario_ids.discard(scenario_id)


def _resolve_token(env, token_attr: str | None) -> str | None:
    if token_attr is None:
        return None
    if token_attr == "wrong_token":
        return "wrong_token"
    return getattr(env, token_attr)


def _scenario_payload(case: str = "valid") -> dict:
    suffix = str(uuid4())
    payload = {
        "name": f"Scenario {suffix}",
        "complexity": "EASY",
        "system_prompt": f"Prompt {suffix}",
        "misc_info": {"seed": suffix},
    }
    if case == "missing_name":
        payload.pop("name")
    elif case == "missing_prompt":
        payload.pop("system_prompt")
    elif case == "invalid_complexity":
        payload["complexity"] = "IMPOSSIBLE"
    return payload


def _scenario_update_payload(case: str = "valid") -> dict:
    suffix = str(uuid4())
    payload = {
        "name": f"Updated {suffix}",
        "system_prompt": f"Updated prompt {suffix}",
    }
    if case == "empty":
        return {}
    return payload


def _hook_email_payload() -> dict:
    suffix = str(uuid4())
    return {
        "subject": f"Hook subject {suffix}",
        "sender_email": f"hook-{suffix[:8]}@test.com",
        "language": "en",
        "body": f"Body {suffix}",
        "variables": {"name": "tester"},
    }


def _hook_email_update_payload(case: str = "valid") -> dict:
    suffix = str(uuid4())
    payload = {
        "subject": f"Updated subject {suffix}",
        "body": f"Updated body {suffix}",
    }
    if case == "empty":
        return {}
    return payload


def _create_owned_scenario(env, scenario_ids: set[str], payload_case: str = "valid", payload: dict | None = None) -> str:
    scenario_payload = payload or _scenario_payload(payload_case)
    response = UserChallengesInteractor.create_scenario(env.user_token, scenario_payload)
    assert response.status_code == 201
    scenario_id = response.json()["id"]
    scenario_ids.add(scenario_id)
    return scenario_id


def _create_hook_email_for_scenario(env, scenario_id: str, payload: dict | None = None) -> dict:
    email_payload = payload or _hook_email_payload()
    response = UserChallengesInteractor.create_hook_email(env.user_token, scenario_id, email_payload)
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def test_env():
    env = init_test()
    scenario_ids: set[str] = set()
    try:
        yield env, scenario_ids
    finally:
        _cleanup_scenarios(env.user_token, scenario_ids)
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
def test_list_scenarios_authorization(test_env, token_attr, expected_status, expect_item):
    env, scenario_ids = test_env
    created_id = None
    if expect_item:
        created_id = _create_owned_scenario(env, scenario_ids)

    token = _resolve_token(env, token_attr)
    response = UserChallengesInteractor.list_scenarios(token)

    assert response.status_code == expected_status
    if expected_status == 200 and created_id:
        items = response.json().get("items", [])
        assert any(item["id"] == created_id for item in items)


@pytest.mark.parametrize(
    "token_attr,payload_case,expected_status",
    [
        ("user_token", "valid", 201),
        ("user_token", "missing_name", 422),
        ("user_token", "missing_prompt", 422),
        ("user_token", "invalid_complexity", 422),
        ("orgadmin_token", "valid", 403),
        ("admin_token", "valid", 403),
        ("wrong_token", "valid", 502),
        (None, "valid", 403),
    ],
    ids=[
        "user_valid",
        "missing_name",
        "missing_prompt",
        "invalid_complexity",
        "orgadmin_forbidden",
        "admin_forbidden",
        "invalid_token",
        "missing_token",
    ],
)
def test_create_scenario_authorization_and_validation(test_env, token_attr, payload_case, expected_status):
    env, scenario_ids = test_env
    payload = _scenario_payload(payload_case)

    token = _resolve_token(env, token_attr)
    response = UserChallengesInteractor.create_scenario(token, payload)

    assert response.status_code == expected_status
    if expected_status == 201:
        created = response.json()
        scenario_ids.add(created["id"])
        assert created["name"] == payload["name"]
        assert created["system_prompt"] == payload["system_prompt"]


@pytest.mark.parametrize(
    "token_attr,scenario_reference,payload_case,expected_status",
    [
        ("user_token", "existing", "valid", 200),
        ("user_token", "existing", "empty", 400),
        ("user_token", "random", "valid", 404),
        ("orgadmin_token", "existing", "valid", 403),
        ("admin_token", "existing", "valid", 403),
        ("wrong_token", "existing", "valid", 502),
        (None, "existing", "valid", 403),
    ],
    ids=[
        "user_ok",
        "user_empty_payload",
        "user_missing_scenario",
        "orgadmin_forbidden",
        "admin_forbidden",
        "invalid_token",
        "missing_token",
    ],
)
def test_update_scenario_responses(test_env, token_attr, scenario_reference, payload_case, expected_status):
    env, scenario_ids = test_env
    scenario_id = (
        _create_owned_scenario(env, scenario_ids) if scenario_reference == "existing" else str(uuid4())
    )
    payload = _scenario_update_payload(payload_case)

    token = _resolve_token(env, token_attr)
    response = UserChallengesInteractor.update_scenario(token, scenario_id, payload)

    assert response.status_code == expected_status
    if expected_status == 200:
        updated = response.json()
        assert updated["id"] == scenario_id
        for field, value in payload.items():
            assert updated[field] == value


@pytest.mark.parametrize(
    "token_attr,scenario_reference,expected_status",
    [
        ("user_token", "existing", 200),
        ("user_token", "random", 404),
        ("orgadmin_token", "existing", 403),
        ("admin_token", "existing", 403),
        ("wrong_token", "existing", 502),
        (None, "existing", 403),
    ],
    ids=[
        "user_ok",
        "user_missing_scenario",
        "orgadmin_forbidden",
        "admin_forbidden",
        "invalid_token",
        "missing_token",
    ],
)
def test_delete_scenario_responses(test_env, token_attr, scenario_reference, expected_status):
    env, scenario_ids = test_env
    if scenario_reference == "existing":
        scenario_id = _create_owned_scenario(env, scenario_ids)
    else:
        scenario_id = str(uuid4())

    token = _resolve_token(env, token_attr)
    response = UserChallengesInteractor.delete_scenario(token, scenario_id)

    assert response.status_code == expected_status
    if expected_status == 200:
        scenario_ids.discard(scenario_id)


@pytest.mark.parametrize(
    "token_attr,email_state,expected_status",
    [
        ("user_token", "fresh", 201),
        ("user_token", "duplicate", 409),
        ("orgadmin_token", "fresh", 403),
        ("admin_token", "fresh", 403),
        ("wrong_token", "fresh", 502),
        (None, "fresh", 403),
    ],
    ids=[
        "user_ok",
        "duplicate",
        "orgadmin_forbidden",
        "admin_forbidden",
        "invalid_token",
        "missing_token",
    ],
)
def test_create_hook_email_responses(test_env, token_attr, email_state, expected_status):
    env, scenario_ids = test_env
    scenario_id = _create_owned_scenario(env, scenario_ids)
    if email_state == "duplicate":
        _create_hook_email_for_scenario(env, scenario_id)

    payload = _hook_email_payload()
    token = _resolve_token(env, token_attr)
    response = UserChallengesInteractor.create_hook_email(token, scenario_id, payload)

    assert response.status_code == expected_status
    if expected_status == 201:
        created = response.json()
        assert created["sender_email"] == payload["sender_email"]
        assert created["role"] == "HOOK"


@pytest.mark.parametrize(
    "token_attr,email_state,payload_case,expected_status",
    [
        ("user_token", "existing", "valid", 200),
        ("user_token", "existing", "empty", 400),
        ("user_token", "missing_email", "valid", 404),
        ("orgadmin_token", "existing", "valid", 403),
        ("wrong_token", "existing", "valid", 502),
        (None, "existing", "valid", 403),
    ],
    ids=[
        "user_ok",
        "user_empty_payload",
        "missing_hook",
        "orgadmin_forbidden",
        "invalid_token",
        "missing_token",
    ],
)
def test_update_hook_email_responses(test_env, token_attr, email_state, payload_case, expected_status):
    env, scenario_ids = test_env
    scenario_id = _create_owned_scenario(env, scenario_ids)
    if email_state == "existing":
        _create_hook_email_for_scenario(env, scenario_id)

    payload = _hook_email_update_payload(payload_case)
    token = _resolve_token(env, token_attr)
    response = UserChallengesInteractor.update_hook_email(token, scenario_id, payload)

    assert response.status_code == expected_status
    if expected_status == 200:
        updated = response.json()
        for field, value in payload.items():
            assert updated[field] == value


@pytest.mark.parametrize(
    "token_attr,email_state,expected_status",
    [
        ("user_token", "existing", 200),
        ("user_token", "missing_email", 404),
        ("orgadmin_token", "existing", 403),
        ("wrong_token", "existing", 502),
        (None, "existing", 403),
    ],
    ids=[
        "user_ok",
        "missing_hook",
        "orgadmin_forbidden",
        "invalid_token",
        "missing_token",
    ],
)
def test_delete_hook_email_responses(test_env, token_attr, email_state, expected_status):
    env, scenario_ids = test_env
    scenario_id = _create_owned_scenario(env, scenario_ids)
    if email_state == "existing":
        _create_hook_email_for_scenario(env, scenario_id)

    token = _resolve_token(env, token_attr)
    response = UserChallengesInteractor.delete_hook_email(token, scenario_id)

    assert response.status_code == expected_status


def test_scenario_export_import_roundtrip(test_env):
    env, scenario_ids = test_env
    payload = _scenario_payload()
    scenario_id = _create_owned_scenario(env, scenario_ids, payload=payload)

    export_response = UserChallengesInteractor.export_scenario(env.user_token, scenario_id)
    assert export_response.status_code == 200
    assert export_response.headers.get("Content-Type", "").startswith("application/json")
    exported_payload = json.loads(export_response.content.decode("utf-8"))
    assert exported_payload["name"] == payload["name"]
    assert exported_payload["system_prompt"] == payload["system_prompt"]

    import_filename = f"import_{uuid4()}.json"
    import_response = UserChallengesInteractor.import_scenario(
        env.user_token,
        import_filename,
        export_response.content,
    )
    assert import_response.status_code == 201
    imported = import_response.json()
    scenario_ids.add(imported["id"])
    assert imported["name"] == payload["name"]
    assert imported["complexity"] == payload["complexity"]


def test_delete_scenario_removes_hook_email(test_env):
    env, scenario_ids = test_env
    scenario_id = _create_owned_scenario(env, scenario_ids)
    created_email = _create_hook_email_for_scenario(env, scenario_id)
    assert created_email["role"] == "HOOK"

    delete_response = UserChallengesInteractor.delete_scenario(env.user_token, scenario_id)
    assert delete_response.status_code == 200
    scenario_ids.discard(scenario_id)

    email_response = UserChallengesInteractor.get_hook_email(env.user_token, scenario_id)
    assert email_response.status_code == 404

    list_response = UserChallengesInteractor.list_scenarios(env.user_token)
    assert list_response.status_code == 200
    remaining = list_response.json().get("items", [])
    assert all(item["id"] != scenario_id for item in remaining)
