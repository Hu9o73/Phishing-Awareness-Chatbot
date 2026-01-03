from uuid import UUID

from app.models.base_models import (
    Challenge,
    ChallengeListResponse,
    ChallengeStatusResponse,
    ChallengeStatusUpdate,
    ChallengeWorkflowResponse,
    ExchangesCountResponse,
    ExchangesResponse,
    LastEmailStatusResponse,
    StatusResponse,
)
from app.models.enum_models import ChallengeStatus
from app.services.Monitoring.monitoring import MonitoringService
from fastapi import APIRouter, Depends, Query, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

router = APIRouter()
security = HTTPBearer()


@router.post("/start-challenge", response_model=Challenge, status_code=status.HTTP_201_CREATED)
async def start_challenge(
    employee_id: UUID,
    scenario_id: UUID,
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Challenge:
    token = credentials.credentials
    return await MonitoringService.start_challenge(token, employee_id, scenario_id)


@router.get("/retrieve-status", response_model=ChallengeStatusResponse)
async def retrieve_status(
    challenge_id: UUID,
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> ChallengeStatusResponse:
    token = credentials.credentials
    return await MonitoringService.retrieve_status(token, challenge_id)


@router.get("/challenges", response_model=ChallengeListResponse)
async def list_challenges(
    status: ChallengeStatus | None = Query(None, description="Optional challenge status filter."),
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> ChallengeListResponse:
    token = credentials.credentials
    return await MonitoringService.list_challenges(token, status)


@router.put("/challenges/status", response_model=Challenge)
async def update_challenge_status(
    challenge_update: ChallengeStatusUpdate,
    challenge_id: UUID,
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Challenge:
    token = credentials.credentials
    return await MonitoringService.update_challenge_status(token, challenge_id, challenge_update)


@router.delete("/challenges", response_model=StatusResponse)
async def delete_challenge(
    challenge_id: UUID,
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> StatusResponse:
    token = credentials.credentials
    return await MonitoringService.delete_challenge(token, challenge_id)


@router.get("/get-exchanges", response_model=ExchangesResponse)
async def get_exchanges(
    challenge_id: UUID, credentials: HTTPAuthorizationCredentials = Depends(security)
) -> ExchangesResponse:
    token = credentials.credentials
    return await MonitoringService.get_exchanges(token, challenge_id)


@router.get("/get-exchanges/count", response_model=ExchangesCountResponse)
async def get_exchanges_count(
    challenge_id: UUID, credentials: HTTPAuthorizationCredentials = Depends(security)
) -> ExchangesCountResponse:
    token = credentials.credentials
    return await MonitoringService.get_exchanges_count(token, challenge_id)


@router.get("/pending-emails/count", response_model=ExchangesCountResponse)
async def get_pending_emails_count(
    user_id: UUID, credentials: HTTPAuthorizationCredentials = Depends(security)
) -> ExchangesCountResponse:
    token = credentials.credentials
    return await MonitoringService.get_pending_email_count_for_user(token, user_id)


@router.post("/send-all-pending", response_model=StatusResponse)
async def send_all_pending_emails(credentials: HTTPAuthorizationCredentials = Depends(security)) -> StatusResponse:
    token = credentials.credentials
    return await MonitoringService.send_all_pending_emails(token)


@router.get("/retrieve-answers", response_model=StatusResponse)
async def retrieve_answers(credentials: HTTPAuthorizationCredentials = Depends(security)) -> StatusResponse:
    token = credentials.credentials
    return await MonitoringService.retrieve_answers(token)


@router.get("/challenge-last-email-status", response_model=LastEmailStatusResponse)
async def get_last_email_status(
    challenge_id: UUID, credentials: HTTPAuthorizationCredentials = Depends(security)
) -> LastEmailStatusResponse:
    token = credentials.credentials
    return await MonitoringService.get_last_email_status(token, challenge_id)


@router.get("/challenges/{challenge_id}", response_model=ChallengeWorkflowResponse)
async def get_challenge_workflow(
    challenge_id: UUID, credentials: HTTPAuthorizationCredentials = Depends(security)
) -> ChallengeWorkflowResponse:
    token = credentials.credentials
    return await MonitoringService.get_challenge_workflow(token, challenge_id)
