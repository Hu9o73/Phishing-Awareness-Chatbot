from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.v1.Admin.Organizations import router as admin_org_router
from app.api.routes.v1.Admin.Users import router as admin_users_router
from app.api.routes.v1.AuthenticationRoutes import router as auth_router
from app.api.routes.v1.health import router as health_router
from app.api.routes.v1.OrgAdmin.OrgMembers import router as orgadmin_orgmembers_router
from app.api.routes.v1.OrgAdmin.Users import router as orgadmin_users_router
from app.Middleware import Middleware

# Initialize FastAPI app with lifespan
app = FastAPI(title="Authentication API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

# Admin routes
app.include_router(
    admin_users_router,
    prefix="/admin",
    tags=["Admin - Users"],
    dependencies=[Depends(Middleware.token_required), Depends(Middleware.is_admin)]
)
app.include_router(
    admin_org_router,
    prefix="/admin",
    tags=["Admin - Organizations"],
    dependencies=[Depends(Middleware.token_required), Depends(Middleware.is_admin)]
)

# OrgAdmin routes
app.include_router(
    orgadmin_users_router,
    prefix="/orgadmin",
    tags=["OrgAdmin - Users"],
    dependencies=[Depends(Middleware.token_required), Depends(Middleware.is_org_admin)]
)
app.include_router(
    orgadmin_orgmembers_router,
    prefix="/orgadmin",
    tags=["OrgAdmin - Organization Members"],
    dependencies=[Depends(Middleware.token_required), Depends(Middleware.is_org_admin)]
)
