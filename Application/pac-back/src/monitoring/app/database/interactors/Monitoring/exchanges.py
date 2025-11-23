from datetime import datetime, timezone
from uuid import UUID

from app.database.client import get_db
from app.models.base_models import Email, EmailCreate
from app.models.enum_models import EmailRole, EmailStatus
from supabase import Client


class MonitoringExchangesInteractor:
    @staticmethod
    async def get_email(email_id: UUID) -> Email | None:
        supabase: Client = get_db()
        response = supabase.table("emails").select("*").eq("id", str(email_id)).limit(1).execute()
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

    @staticmethod
    @staticmethod
    async def list_emails_for_target(
        scenario_id: UUID, target_id: UUID, status: EmailStatus | None = None, challenge_id: UUID | None = None
    ) -> list[Email]:
        supabase: Client = get_db()
        query = (
            supabase.table("emails")
            .select("*")
            .eq("scenario_id", str(scenario_id))
            .eq("target_id", str(target_id))
            .order("created_at", desc=False)
        )
        if status is not None:
            query = query.eq("status", status.value)
        if challenge_id is not None:
            query = query.eq("challenge_id", str(challenge_id))
        response = query.execute()
        if not response.data:
            return []
        return [Email(**entry) for entry in response.data]

    @staticmethod
    async def update_exchange_status(exchange_id: UUID, status: EmailStatus) -> Email | None:
        supabase: Client = get_db()
        response = (
            supabase.table("emails")
            .update(
                {"status": status.value, "updated_at": datetime.now(timezone.utc).isoformat()}
            )
            .eq("id", str(exchange_id))
            .execute()
        )
        if not response.data:
            return None
        return Email(**response.data[0])

    @staticmethod
    async def create_email_in_db(email_data: EmailCreate) -> Email:
        supabase: Client = get_db()
        payload = email_data.model_dump(exclude_none=True)
        payload["scenario_id"] = str(email_data.scenario_id)
        payload["role"] = email_data.role.value
        # Discuss the need for this section given the use of exclude_none
        if email_data.id is not None:
            payload["id"] = str(email_data.id)
        if email_data.target_id is not None:
            payload["target_id"] = str(email_data.target_id)
        if email_data.previous_email is not None:
            payload["previous_email"] = str(email_data.previous_email)
        if email_data.status is not None:
            payload["status"] = email_data.status.value
        if email_data.challenge_id is not None:
            payload["challenge_id"] = str(email_data.challenge_id)

        response = supabase.table("emails").upsert(payload).execute()
        if not response.data:
            raise ValueError("Failed to create email exchange")
        return Email(**response.data[0])

    @staticmethod
    async def update_email_send_info(exchange_id: UUID, challenge_id: UUID | None, status: EmailStatus) -> Email | None:
        supabase: Client = get_db()
        update_payload = {"status": status.value, "updated_at": datetime.now(timezone.utc).isoformat()}
        if challenge_id:
            update_payload["challenge_id"] = str(challenge_id)
        response = (supabase.table("emails").update(update_payload).eq("id", str(exchange_id)).execute())
        if not response.data:
            return None
        return Email(**response.data[0])

    @staticmethod
    async def get_latest_by_challenge_before(challenge_id: UUID, before: datetime) -> Email | None:
        supabase: Client = get_db()
        response = (
            supabase.table("emails")
            .select("*")
            .eq("challenge_id", str(challenge_id))
            .lte("created_at", before.isoformat())
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
        if not response.data:
            return None
        return Email(**response.data[0])

    @staticmethod
    async def get_latest_received_email() -> Email | None:
        supabase: Client = get_db()
        response = (
            supabase.table("emails")
            .select("*")
            .eq("status", EmailStatus.RECIEVED.value)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )
        if not response.data:
            return None
        return Email(**response.data[0])
