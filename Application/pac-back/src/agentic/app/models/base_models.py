from datetime import datetime
from typing import Literal
from uuid import UUID

from app.models.enum_models import ChallengeStatus, ChannelEnum, Complexity, EmailRole, EmailStatus, RoleEnum
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
    status: EmailStatus | None = None
    challenge_id: UUID | None = None
    updated_at: datetime | None = None
    created_at: datetime | None = None


class EmailCreate(BaseModel):
    id: UUID | None = None
    scenario_id: UUID
    role: EmailRole
    sender_email: str
    language: str
    target_id: UUID | None = None
    previous_email: UUID | None = None
    subject: str | None = None
    body: str | None = None
    variables: dict | None = None
    status: EmailStatus | None = None
    challenge_id: UUID | None = None


class AgenticFlowResponse(BaseModel):
    email_id: UUID
    subject: str | None = None
    body: str | None = None
    challenge_status: ChallengeStatus
    score: int | None = None


class HookEmailGenerationResponse(BaseModel):
    subject: str | None = None
    body: str


class MessageModel(BaseModel):
    message: str
    created_at: datetime
