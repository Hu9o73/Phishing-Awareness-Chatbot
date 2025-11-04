from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from app.database.client import get_db
from app.models.base_models import Scenario, ScenarioCreate, ScenarioUpdate
from supabase import Client


class UserScenariosInteractor:
    @staticmethod
    async def create_scenario(organization_id: UUID, scenario: ScenarioCreate) -> Scenario:
        supabase: Client = get_db()
        payload: dict[str, Any] = scenario.model_dump(exclude_none=True)
        if "misc_info" not in payload:
            payload["misc_info"] = {}
        payload["organization_id"] = str(organization_id)

        response = supabase.table("scenarios").insert(payload).execute()
        if not response.data:
            raise ValueError("Failed to create scenario")
        return Scenario(**response.data[0])

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

    @staticmethod
    async def list_scenarios(organization_id: UUID) -> list[Scenario]:
        supabase: Client = get_db()
        response = (
            supabase.table("scenarios")
            .select("*")
            .eq("organization_id", str(organization_id))
            .execute()
        )
        if not response.data:
            return []
        return [Scenario(**entry) for entry in response.data]

    @staticmethod
    async def update_scenario(
        organization_id: UUID, scenario_id: UUID, scenario_update: ScenarioUpdate
    ) -> Scenario | None:
        supabase: Client = get_db()
        update_payload: dict[str, Any] = scenario_update.model_dump(exclude_unset=True, exclude_none=True)
        if not update_payload:
            return await UserScenariosInteractor.get_scenario(organization_id, scenario_id)

        update_payload["updated_at"] = datetime.now(timezone.utc).isoformat()

        response = (
            supabase.table("scenarios")
            .update(update_payload)
            .eq("organization_id", str(organization_id))
            .eq("id", str(scenario_id))
            .execute()
        )
        if not response.data:
            return None
        return Scenario(**response.data[0])

    @staticmethod
    async def delete_scenario(organization_id: UUID, scenario_id: UUID) -> None:
        supabase: Client = get_db()
        _ = (
            supabase.table("scenarios")
            .delete()
            .eq("organization_id", str(organization_id))
            .eq("id", str(scenario_id))
            .execute()
        )
