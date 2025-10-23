from uuid import UUID

from app.database.client import get_db
from app.models.base_models import OrganizationCreationModel, OrganizationModel, StatusResponse
from fastapi import HTTPException, status
from supabase import Client


class AdminOrganizationInteractor:
    @staticmethod
    async def create_organization(organization: OrganizationCreationModel) -> OrganizationModel:
        supabase: Client = get_db()

        # Insert new organization
        response = (
            supabase.table("organizations")
            .insert({"name": organization.name, "description": organization.description})
            .execute()
        )

        return OrganizationModel(**response.data[0])

    @staticmethod
    async def list_organizations(org_id: UUID | None = None) -> list[OrganizationModel]:
        supabase: Client = get_db()
        response = supabase.table("organizations").select("*")
        if org_id:
            response = response.eq("organization_id", org_id).limit(1)
        response = response.execute()
        return [OrganizationModel(**organization) for organization in response.data]

    @staticmethod
    async def delete_organization(org_id: UUID) -> StatusResponse:
        supabase: Client = get_db()

        # First clean members and users (cascade)
        supabase.table("org_members").delete().eq("organization_id", org_id).execute()
        supabase.table("users").delete().eq("organization_id", org_id).execute()

        # Then delete organization
        supabase.table("organizations").delete().eq("id", org_id).execute()
        return StatusResponse(status="ok", message=f"Succesfully delete organization with id {org_id}")
