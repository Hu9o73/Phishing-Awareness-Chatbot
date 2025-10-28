from app.models.base_models import HealthResponse
from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check() -> HealthResponse:
    return HealthResponse(status="ok")
