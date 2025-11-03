from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from app.database.client import get_db
from app.models.base_models import Email, HookEmailCreate, HookEmailUpdate
from app.models.enum_models import EmailRole
from supabase import Client


class UserEmailsInteractor:
    @staticmethod
    async def create_hook_email(scenario_id: UUID, email_data: HookEmailCreate) -> Email:
        supabase: Client = get_db()
        payload: dict[str, Any] = email_data.model_dump(exclude_none=True)
        payload["role"] = EmailRole.HOOK.value
        payload["scenario_id"] = str(scenario_id)
        payload["target_id"] = None
        payload["previous_email"] = None

        response = supabase.table("emails").insert(payload).execute()
        if not response.data:
            raise ValueError("Failed to create hook email")
        return Email(**response.data[0])

    @staticmethod
    async def get_hook_email(scenario_id: UUID) -> Email | None:
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

    @staticmethod
    async def update_hook_email(scenario_id: UUID, email_update: HookEmailUpdate) -> Email | None:
        supabase: Client = get_db()
        update_payload: dict[str, Any] = email_update.model_dump(exclude_unset=True, exclude_none=True)
        if not update_payload:
            return await UserEmailsInteractor.get_hook_email(scenario_id)

        update_payload["updated_at"] = datetime.now(timezone.utc).isoformat()
        update_payload["target_id"] = None
        update_payload["previous_email"] = None

        response = (
            supabase.table("emails")
            .update(update_payload)
            .eq("scenario_id", str(scenario_id))
            .eq("role", EmailRole.HOOK.value)
            .select("*")
            .execute()
        )
        if not response.data:
            return None
        return Email(**response.data[0])

    @staticmethod
    async def delete_hook_email(scenario_id: UUID) -> None:
        supabase: Client = get_db()
        supabase.table("emails").delete().eq("scenario_id", str(scenario_id)).eq(
            "role", EmailRole.HOOK.value
        ).execute()

    @staticmethod
    async def delete_all_for_scenario(scenario_id: UUID) -> None:
        supabase: Client = get_db()
        supabase.table("emails").delete().eq("scenario_id", str(scenario_id)).execute()

    @staticmethod
    async def delete_all_for_scenarios(scenario_ids: list[UUID]) -> None:
        if not scenario_ids:
            return
        supabase: Client = get_db()
        supabase.table("emails").delete().in_(
            "scenario_id", [str(scenario_id) for scenario_id in scenario_ids]
        ).execute()
