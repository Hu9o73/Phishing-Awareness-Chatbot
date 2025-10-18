from datetime import datetime
from typing import Literal
from uuid import UUID

from app.common.enum_models import RoleEnum
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: Literal["ok"]


class UserModel(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    role: RoleEnum
    credits: int
    organization_id: UUID | None
    updated_at: datetime
    created_at: datetime


class PublicUserModel(BaseModel):
    id: UUID | None
    email: str | None
    first_name: str | None
    last_name: str | None
    role: RoleEnum | None
    credits: int | None
    created_at: datetime | None


class MemberModel(BaseModel):
    id: UUID
    organization_id: UUID
    first_name: str
    last_name: str
    email: str
    updated_at: datetime
    created_at: datetime


class OrganizationModel(BaseModel):
    id: UUID
    name: str
    description: str | None
    updated_at: datetime
    created_at: datetime
