from app.database.interactors.Base.authentication import AuthenticationInteractor
from app.models.base_models import HealthResponse
from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/hack/hash")
async def hash_password_hack(password: str) -> str:
    return await AuthenticationInteractor.password_hasher(password)
