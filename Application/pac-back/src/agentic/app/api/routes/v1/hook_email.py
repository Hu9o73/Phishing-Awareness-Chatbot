from uuid import UUID

from app.models.base_models import HookEmailGenerationResponse
from app.services.hook_emailer_service import HookEmailerService
from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

router = APIRouter()
security = HTTPBearer()


@router.post("/generate-hook-email", response_model=HookEmailGenerationResponse, status_code=status.HTTP_201_CREATED)
async def generate_hook_email(
    scenario_id: UUID, credentials: HTTPAuthorizationCredentials = Depends(security)
) -> HookEmailGenerationResponse:
    token = credentials.credentials
    return await HookEmailerService.generate_hook_email(token, scenario_id)
