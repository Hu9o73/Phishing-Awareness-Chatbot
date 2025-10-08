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
    updated_at: datetime
    created_at: datetime
