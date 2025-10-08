from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel

from app.common.enum_models import RoleEnum

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
