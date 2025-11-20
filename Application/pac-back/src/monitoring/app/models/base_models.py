from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID

from app.models.enum_models import ChallengeStatus, ChannelEnum, Complexity, EmailRole, RoleEnum
from pydantic import BaseModel


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


class OrgMemberModel(BaseModel):
    id: UUID
    organization_id: UUID
    first_name: str
    last_name: str
    email: str
    updated_at: datetime | None = None
    created_at: datetime | None = None


class Scenario(BaseModel):
    id: UUID
    organization_id: UUID
    name: str
    complexity: Complexity
    system_prompt: str
    misc_info: dict | None = None
    updated_at: datetime | None = None
    created_at: datetime | None = None


class Challenge(BaseModel):
    id: UUID
    user_id: UUID
    employee_id: UUID
    scenario_id: UUID
    channel: ChannelEnum
    status: ChallengeStatus
    score: float | None = None
    last_exchange_id: UUID | None = None
    updated_at: datetime | None = None
    created_at: datetime | None = None


class ChallengeStatusResponse(BaseModel):
    status: ChallengeStatus


class Email(BaseModel):
    id: UUID
    scenario_id: UUID
    role: EmailRole
    target_id: UUID | None = None
    previous_email: UUID | None = None
    subject: str | None = None
    sender_email: str
    language: str
    body: str | None = None
    variables: dict | None = None
    updated_at: datetime | None = None
    created_at: datetime | None = None


class ExchangesResponse(BaseModel):
    exchanges: list[Email]
