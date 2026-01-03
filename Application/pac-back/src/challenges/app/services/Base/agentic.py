import os
from uuid import UUID

import dotenv
import requests
from app.models.base_models import HookEmailGenerationResponse
from fastapi import HTTPException, status
from requests import RequestException

dotenv.load_dotenv()


class AgenticServiceClient:
    """Client used to interact with the agentic service from the challenges service."""

    _DEFAULT_BASE_URL = "http://pac-agentic:8004"

    @staticmethod
    def _build_url(path: str) -> str:
        base_url = os.getenv("AGENTIC_SERVICE_URL", AgenticServiceClient._DEFAULT_BASE_URL)
        return f"{base_url.rstrip('/')}{path}"

    @staticmethod
    def _extract_detail(response: requests.Response) -> str:
        detail = "Agentic service request failed"
        try:
            payload = response.json()
            if isinstance(payload, dict):
                detail = payload.get("detail", detail)
        except ValueError:
            pass
        return detail

    @staticmethod
    def generate_hook_email(token: str, scenario_id: UUID) -> HookEmailGenerationResponse:
        url = AgenticServiceClient._build_url("/generate-hook-email")
        try:
            response = requests.post(
                url, params={"scenario_id": str(scenario_id)}, headers={"Authorization": f"Bearer {token}"}, timeout=30.0
            )
        except RequestException as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Agentic service is unavailable",
            ) from exc

        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=AgenticServiceClient._extract_detail(response),
            ) from exc

        try:
            payload = response.json()
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Invalid response from agentic service",
            ) from exc

        try:
            return HookEmailGenerationResponse(**payload)
        except TypeError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Invalid hook email payload received from agentic service",
            ) from exc
