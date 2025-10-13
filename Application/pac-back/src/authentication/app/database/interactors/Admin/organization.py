from app.database.client import get_db
from app.models.base_models import OrganizationCreationModel, OrganizationModel
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
