from uuid import UUID

from app.database.client import get_db
from app.models.base_models import OrgMemberModel


class OrgMembersInteractor:
    @staticmethod
    async def list_members_by_organization(organization_id: UUID) -> list[OrgMemberModel]:
        supabase = get_db()
        response = (
            supabase.table("org_members")
            .select("*")
            .eq("organization_id", str(organization_id))
            .execute()
        )
        if not response.data:
            return []
        return [OrgMemberModel(**member) for member in response.data]
