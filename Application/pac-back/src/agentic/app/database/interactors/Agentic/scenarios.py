from uuid import UUID

from app.database.client import get_db
from app.models.base_models import Scenario
from supabase import Client


class AgenticScenariosInteractor:
    @staticmethod
    async def get_scenario(organization_id: UUID, scenario_id: UUID) -> Scenario | None:
        supabase: Client = get_db()
        response = (
            supabase.table("scenarios")
            .select("*")
            .eq("organization_id", str(organization_id))
            .eq("id", str(scenario_id))
            .limit(1)
            .execute()
        )
        if not response.data:
            return None
        return Scenario(**response.data[0])
