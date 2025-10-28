from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

from app.models.enum_models import RoleEnum
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: Literal["ok"]


class StatusResponse(BaseModel):
    status: Literal["ok", "error"]
    message: str


class JWTModel(BaseModel):
    user_id: str
    exp: datetime


class PublicUserModel(BaseModel):
    id: UUID | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    role: RoleEnum | None = None
    credits: int | None = None
    organization_id: UUID | None = None
    created_at: datetime | None = None
