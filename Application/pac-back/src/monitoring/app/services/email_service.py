from __future__ import annotations

import os
import re
from typing import Any
from uuid import UUID

import resend
from app.models.base_models import SentEmailReference
from fastapi import HTTPException, status
from resend import exceptions as resend_exceptions


# TODO: Implement an actual class service, with the api key as self variable
def _configure_resend() -> None:
    api_key = os.getenv("RESEND_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Resend API key is not configured."
        )
    resend.api_key = api_key


def _inject_challenge_marker(html: str | None, challenge_id: str) -> str:
    marker = f'data-pac-challenge-id="{challenge_id}"'
    if html and marker in html:
        return html
    hidden_span = (
        f'<span {marker} style="display:none; color:transparent; font-size:0;" aria-hidden="true">.</span>'
    )
    return (html or "") + hidden_span


def extract_challenge_id_from_html(html: str | None) -> str | None:
    if not html:
        return None
    match = re.search(r'data-pac-challenge-id="([^"]+)"', html)
    if match:
        return match.group(1).strip()
    return None


def send_email(
    target_email: str, subject: str | None, body: str | None, sender_email: str, challenge_id: str
) -> SentEmailReference | None:
    _configure_resend()
    html = _inject_challenge_marker(body, challenge_id)
    params: dict[str, Any] = {
        "from": "hugo@onboarding.phishward.com", # To be replaced by sender_email in the future
        "to": [target_email],
        "subject": subject or "",
        "html": html,
    }
    try:
        response = resend.Emails.send(params)
        sent_id = getattr(response, "id", None)
    except resend_exceptions.ResendError as exc:
        # Once domains are managed by the PAC, remove and handle the domain error
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to send email via Resend.",
        ) from exc

    return SentEmailReference(UUID(sent_id), UUID(challenge_id))


def list_incoming_replies(after: str | None = None) -> dict[str, Any]:
    _configure_resend()
    try:
        params = {"after": after} if after else None
        response = resend.Emails.Receiving.list(params=params)
    except resend_exceptions.ResendError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY, detail="Failed to retrieve incoming replies from Resend."
        ) from exc

    return response


def get_received_email(email_id: str) -> dict[str, Any]:
    _configure_resend()
    try:
        response = resend.Emails.Receiving.get(email_id=email_id)
        print("RESPONSE ", response)
    except resend_exceptions.ResendError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY, detail="Failed to retrieve received email."
        ) from exc
    return response if isinstance(response, dict) else response.__dict__
