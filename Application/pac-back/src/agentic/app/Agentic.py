from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.v1.agentic_flow import router as agentic_router
from app.api.routes.v1.hook_email import router as hook_email_router
from app.api.routes.v1.health import router as health_router
from app.api.routes.v1.messages import router as message_router

app = FastAPI(title="Agentic API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, tags=["Health"])
app.include_router(message_router, tags=["Messages"])
app.include_router(agentic_router, tags=["Agentic"])
app.include_router(hook_email_router, tags=["Agentic"])
