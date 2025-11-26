from uuid import UUID

from app.models.base_models import AgenticFlowResponse
from app.services.agentic_flow_service import AgenticFlowService
from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

router = APIRouter()
security = HTTPBearer()


@router.post("/email-agentic-flow", response_model=AgenticFlowResponse, status_code=status.HTTP_201_CREATED)
async def run_email_agentic_flow(
    challenge_id: UUID, credentials: HTTPAuthorizationCredentials = Depends(security)
) -> AgenticFlowResponse:
    token = credentials.credentials
    return await AgenticFlowService.run_email_flow(token, challenge_id)
