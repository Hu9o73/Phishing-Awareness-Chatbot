from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.v1.health import router as health_router
from app.api.routes.v1.User.OrgMembers import router as user_org_members_router
from app.api.routes.v1.User.Scenarios import router as user_scenarios_router
from app.Middleware import Middleware

# Initialize FastAPI app with lifespan
app = FastAPI(title="Challenges API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(
    user_org_members_router,
    prefix="/user",
    tags=["User - Organization Members"],
    dependencies=[Depends(Middleware.token_required), Depends(Middleware.is_user)],
)
app.include_router(
    user_scenarios_router,
    prefix="/user",
    tags=["User - Scenarios"],
    dependencies=[Depends(Middleware.token_required), Depends(Middleware.is_user)],
)
