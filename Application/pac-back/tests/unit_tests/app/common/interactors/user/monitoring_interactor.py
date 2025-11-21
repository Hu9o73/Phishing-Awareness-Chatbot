from __future__ import annotations

from uuid import UUID

import requests
from app.common.settings import settings


class UserMonitoringInteractor:
    _BASE_URL = settings.MONITORING_URL

    @staticmethod
    def _build_headers(token: str | None) -> dict[str, str]:
        headers: dict[str, str] = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    @staticmethod
    def start_challenge(token: str | None, employee_id: UUID, scenario_id: UUID):
        headers = UserMonitoringInteractor._build_headers(token)
        return requests.post(
            f"{UserMonitoringInteractor._BASE_URL}/start-challenge",
            headers=headers,
            params={
                "employee_id": str(employee_id),
                "scenario_id": str(scenario_id),
            },
        )

    @staticmethod
    def retrieve_status(token: str | None, challenge_id: UUID):
        headers = UserMonitoringInteractor._build_headers(token)
        return requests.get(
            f"{UserMonitoringInteractor._BASE_URL}/retrieve-status",
            headers=headers,
            params={"challenge_id": str(challenge_id)},
        )

    @staticmethod
    def list_challenges(token: str | None, status: str | None = None):
        headers = UserMonitoringInteractor._build_headers(token)
        params = {}
        if status is not None:
            params["status"] = status
        return requests.get(f"{UserMonitoringInteractor._BASE_URL}/challenges", headers=headers, params=params)

    @staticmethod
    def get_exchanges(token: str | None, challenge_id: UUID):
        headers = UserMonitoringInteractor._build_headers(token)
        return requests.get(
            f"{UserMonitoringInteractor._BASE_URL}/get-exchanges",
            headers=headers,
            params={"challenge_id": str(challenge_id)},
        )
