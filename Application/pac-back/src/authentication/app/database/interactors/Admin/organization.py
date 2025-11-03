from uuid import UUID

from app.database.client import get_db
from app.models.base_models import OrganizationCreationModel, OrganizationModel, StatusResponse
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
            response = response.eq("id", org_id).limit(1)
        response = response.execute()
        return [OrganizationModel(**organization) for organization in response.data]

    @staticmethod
    async def delete_organization(org_id: UUID) -> StatusResponse:
        supabase: Client = get_db()
        org_id_str = str(org_id)

        # Delete scenarios and their emails
        scenarios_response = supabase.table("scenarios").select("id").eq("organization_id", org_id_str).execute()
        scenario_entries = scenarios_response.data or []
        scenario_ids = [entry["id"] for entry in scenario_entries if "id" in entry]

        for scenario_id in scenario_ids:
            supabase.table("emails").delete().eq("scenario_id", scenario_id).execute()

        supabase.table("scenarios").delete().eq("organization_id", org_id_str).execute()

        # First clean members and users (cascade)
        supabase.table("org_members").delete().eq("organization_id", org_id_str).execute()
        supabase.table("users").delete().eq("organization_id", org_id_str).execute()

        # Then delete organization
        supabase.table("organizations").delete().eq("id", org_id_str).execute()
        return StatusResponse(status="ok", message=f"Succesfully delete organization with id {org_id}")
