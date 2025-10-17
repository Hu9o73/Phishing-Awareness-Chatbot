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


class LoginResponse(BaseModel):
    access_token: str


class UserModel(BaseModel):
    id: UUID
    email: str
    password: str
    first_name: str
    last_name: str
    role: RoleEnum
    credits: int
    organization_id: UUID
    updated_at: datetime
    created_at: datetime


class UserCreationModel(BaseModel):
    email: str = Field(..., description="Email address", example="john@example.com")
    password: str = Field(..., description="Password", example="mypassword123")
    credits: Optional[int] = Field(default=0, description="Starting credits for the user.", example=20)
    first_name: str = Field(..., description="First name", example="John")
    last_name: str = Field(..., description="Last name", example="Doe")
    role: Optional[RoleEnum] = Field(RoleEnum.MEMBER, description="Role of the user", example="MEMBER")
    organization_id: Optional[UUID] = Field(None, description="UUID of user's org")


class UserListModel(BaseModel):
    id: UUID | None
    email: str | None
    first_name: str | None
    last_name: str | None
    role: RoleEnum | None
    credits: int | None
    created_at: datetime | None


class UserModificationModel(BaseModel):
    email: Optional[str] = Field(default=None)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)


class OrganizationCreationModel(BaseModel):
    name: str = Field(..., description="Name of the organization", example="Woodpecker Creations")
    description: Optional[str] = Field(default=None, description="Description of the organization", examples="My org")


class OrganizationModel(BaseModel):
    id: UUID
    name: str
    description: str | None
    updated_at: datetime
    created_at: datetime


class OrgMemberCreationModel(BaseModel):
    email: str = Field(..., description="Email address", example="john@example.com")
    first_name: str = Field(..., description="First name", example="John")
    last_name: str = Field(..., description="Last name", example="Doe")
    organization_id: Optional[UUID] = Field(None, description="UUID of member's org")


class OrgMemberModel(BaseModel):
    id: UUID
    organization_id: UUID
    first_name: str
    last_name: str
    email: str
    updated_at: datetime
    created_at: datetime
