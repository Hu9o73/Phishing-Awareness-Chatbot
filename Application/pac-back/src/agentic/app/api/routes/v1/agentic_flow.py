from uuid import UUID

from app.models.base_models import AgenticFlowResponse, StatusResponse
from app.services.agentic_flow_service import AgenticFlowService
from fastapi import APIRouter, Depends, Header, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

router = APIRouter()
security = HTTPBearer()


@router.post("/email-agentic-flow", response_model=AgenticFlowResponse, status_code=status.HTTP_201_CREATED)
async def run_email_agentic_flow(
    challenge_id: UUID, credentials: HTTPAuthorizationCredentials = Depends(security)
) -> AgenticFlowResponse:
    token = credentials.credentials
    return await AgenticFlowService.run_email_flow(token, challenge_id)


@router.post("/email-agentic-flow-all", response_model=StatusResponse)
async def run_all_email_agentic_flows(
    super_clock_token: str | None = Header(None, alias="X-Super-Clock-Token"),
) -> StatusResponse:
    return await AgenticFlowService.run_pending_email_flows(super_clock_token)
