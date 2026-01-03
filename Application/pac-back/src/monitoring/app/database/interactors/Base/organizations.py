from uuid import UUID

from app.database.client import get_db
from supabase import Client


class OrganizationsInteractor:
    @staticmethod
    async def list_organization_ids() -> list[UUID]:
        supabase: Client = get_db()
        response = supabase.table("organizations").select("id").execute()
        if not response.data:
            return []
        return [UUID(organization["id"]) for organization in response.data if organization.get("id")]
