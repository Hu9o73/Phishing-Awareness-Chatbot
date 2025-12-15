import os
from uuid import UUID

import dotenv
import requests
from app.models.base_models import Email
from fastapi import HTTPException, status
from requests import RequestException

dotenv.load_dotenv()


class MonitoringServiceClient:
    """Client used to interact with the monitoring service from the agentic service."""

    _DEFAULT_BASE_URL = "http://pac-monitoring:8003"

    @staticmethod
    def _build_url(path: str) -> str:
        base_url = os.getenv("MONITORING_SERVICE_URL", MonitoringServiceClient._DEFAULT_BASE_URL)
        return f"{base_url.rstrip('/')}{path}"

    @staticmethod
    def _extract_detail(response: requests.Response) -> str:
        detail = "Monitoring service request failed"
        try:
            payload = response.json()
            if isinstance(payload, dict):
                detail = payload.get("detail", detail)
        except ValueError:
            pass
        return detail

    @staticmethod
    def get_exchanges(token: str, challenge_id: UUID) -> list[Email]:
        url = MonitoringServiceClient._build_url("/get-exchanges")
        try:
            response = requests.get(
                url, params={"challenge_id": str(challenge_id)}, headers={"Authorization": f"Bearer {token}"}, timeout=5.0
            )
        except RequestException as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Monitoring service is unavailable",
            ) from exc

        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=MonitoringServiceClient._extract_detail(response),
            ) from exc

        try:
            payload = response.json()
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Invalid response from monitoring service",
            ) from exc

        exchanges_payload = payload.get("exchanges", [])
        exchanges: list[Email] = []
        for entry in exchanges_payload:
            try:
                exchanges.append(Email(**entry))
            except TypeError:
                continue
        return exchanges
