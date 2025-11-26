from app.models.base_models import HealthResponse
from fastapi import APIRouter

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok")
