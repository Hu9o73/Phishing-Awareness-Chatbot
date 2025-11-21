from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.v1.health import router as health_router
from app.api.routes.v1.monitoring import router as monitoring_router
from app.Middleware import Middleware

app = FastAPI(title="Monitoring API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(
    monitoring_router,
    tags=["Monitoring"],
    dependencies=[Depends(Middleware.token_required), Depends(Middleware.is_user)],
)
