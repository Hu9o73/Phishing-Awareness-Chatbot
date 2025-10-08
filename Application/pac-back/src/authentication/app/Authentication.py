from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.v1.health import router as health_router
from app.api.routes.v1.AuthenticationRoutes import router as auth_router
from app.api.routes.v1.Users import router as users_router


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
app.include_router(users_router, tags=["Users"])
