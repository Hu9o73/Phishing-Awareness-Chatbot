from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.v1.health import router as health_router
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
