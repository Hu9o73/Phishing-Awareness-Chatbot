from __future__ import annotations

from typing import Any

import requests
from app.common.settings import settings


class UserChallengesInteractor:
    _BASE_URL = f"{settings.CHALLENGES_URL}/user"

    @staticmethod
    def _build_headers(token: str | None) -> dict[str, str]:
        headers: dict[str, str] = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    @staticmethod
    def list_org_members(token: str | None, member_id: str | None = None):
        headers = UserChallengesInteractor._build_headers(token)
        params: dict[str, str] = {}
        if member_id is not None:
            params["id"] = member_id
        return requests.get(f"{UserChallengesInteractor._BASE_URL}/organization/members", headers=headers, params=params)

    @staticmethod
    def list_scenarios(token: str | None, scenario_id: str | None = None):
        headers = UserChallengesInteractor._build_headers(token)
        params: dict[str, str] = {}
        if scenario_id is not None:
            params["id"] = scenario_id
        return requests.get(f"{UserChallengesInteractor._BASE_URL}/scenarios", headers=headers, params=params)

    @staticmethod
    def create_scenario(token: str | None, payload: dict[str, Any]):
        headers = UserChallengesInteractor._build_headers(token)
        return requests.post(
            f"{UserChallengesInteractor._BASE_URL}/scenarios",
            headers=headers,
            json=payload,
        )

    @staticmethod
    def update_scenario(token: str | None, scenario_id: str, payload: dict[str, Any]):
        headers = UserChallengesInteractor._build_headers(token)
        return requests.put(
            f"{UserChallengesInteractor._BASE_URL}/scenarios",
            headers=headers,
            params={"scenario_id": scenario_id},
            json=payload,
        )

    @staticmethod
    def delete_scenario(token: str | None, scenario_id: str):
        headers = UserChallengesInteractor._build_headers(token)
        return requests.delete(
            f"{UserChallengesInteractor._BASE_URL}/scenarios",
            headers=headers,
            params={"scenario_id": scenario_id},
        )

    @staticmethod
    def create_hook_email(token: str | None, scenario_id: str, payload: dict[str, Any]):
        headers = UserChallengesInteractor._build_headers(token)
        return requests.post(
            f"{UserChallengesInteractor._BASE_URL}/scenarios/hook-email",
            headers=headers,
            params={"scenario_id": scenario_id},
            json=payload,
        )

    @staticmethod
    def get_hook_email(token: str | None, scenario_id: str):
        headers = UserChallengesInteractor._build_headers(token)
        return requests.get(
            f"{UserChallengesInteractor._BASE_URL}/scenarios/hook-email",
            headers=headers,
            params={"scenario_id": scenario_id},
        )

    @staticmethod
    def update_hook_email(token: str | None, scenario_id: str, payload: dict[str, Any]):
        headers = UserChallengesInteractor._build_headers(token)
        return requests.put(
            f"{UserChallengesInteractor._BASE_URL}/scenarios/hook-email",
            headers=headers,
            params={"scenario_id": scenario_id},
            json=payload,
        )

    @staticmethod
    def delete_hook_email(token: str | None, scenario_id: str):
        headers = UserChallengesInteractor._build_headers(token)
        return requests.delete(
            f"{UserChallengesInteractor._BASE_URL}/scenarios/hook-email",
            headers=headers,
            params={"scenario_id": scenario_id},
        )

    @staticmethod
    def export_scenario(token: str | None, scenario_id: str):
        headers = UserChallengesInteractor._build_headers(token)
        return requests.get(
            f"{UserChallengesInteractor._BASE_URL}/scenarios/export",
            headers=headers,
            params={"scenario_id": scenario_id},
        )

    @staticmethod
    def import_scenario(token: str | None, filename: str, content: bytes):
        headers = UserChallengesInteractor._build_headers(token)
        files = {
            "file": (filename, content, "application/json"),
        }
        return requests.post(
            f"{UserChallengesInteractor._BASE_URL}/scenarios/import",
            headers=headers,
            files=files,
        )
