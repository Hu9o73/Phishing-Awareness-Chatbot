from uuid import UUID

from app.models.base_models import Challenge, ChallengeStatusResponse, ExchangesResponse
from app.services.Monitoring.monitoring import MonitoringService
from fastapi import APIRouter, Depends, status
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


@router.get("/get-exchanges", response_model=ExchangesResponse)
async def get_exchanges(
    challenge_id: UUID,
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> ExchangesResponse:
    token = credentials.credentials
    return await MonitoringService.get_exchanges(token, challenge_id)
