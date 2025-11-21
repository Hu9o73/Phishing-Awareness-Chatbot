from uuid import UUID

from app.database.client import get_db
from app.models.base_models import Email
from app.models.enum_models import EmailRole
from supabase import Client


class MonitoringExchangesInteractor:
    @staticmethod
    async def get_exchange(exchange_id: UUID) -> Email | None:
        supabase: Client = get_db()
        response = supabase.table("emails").select("*").eq("id", str(exchange_id)).limit(1).execute()
        if not response.data:
            return None
        return Email(**response.data[0])

    @staticmethod
    async def get_hook_exchange_for_scenario(scenario_id: UUID) -> Email | None:
        supabase: Client = get_db()
        response = (
            supabase.table("emails")
            .select("*")
            .eq("scenario_id", str(scenario_id))
            .eq("role", EmailRole.HOOK.value)
            .limit(1)
            .execute()
        )
        if not response.data:
            return None
        return Email(**response.data[0])
