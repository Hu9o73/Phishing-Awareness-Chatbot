from datetime import datetime, timezone
from uuid import UUID

from app.database.client import get_db
from app.models.base_models import Email, EmailCreate
from app.models.enum_models import EmailStatus
from supabase import Client


class AgenticEmailsInteractor:
    @staticmethod
    async def get_email(email_id: UUID) -> Email | None:
        supabase: Client = get_db()
        response = supabase.table("emails").select("*").eq("id", str(email_id)).limit(1).execute()
        if not response.data:
            return None
        return Email(**response.data[0])

    @staticmethod
    async def create_email_in_db(email_data: EmailCreate) -> Email:
        supabase: Client = get_db()
        payload = email_data.model_dump(exclude_none=True)
        payload["scenario_id"] = str(email_data.scenario_id)
        payload["role"] = email_data.role.value
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
    async def update_email_status(email_id: UUID, status: EmailStatus) -> Email | None:
        supabase: Client = get_db()
        response = (
            supabase.table("emails")
            .update({"status": status.value, "updated_at": datetime.now(timezone.utc).isoformat()})
            .eq("id", str(email_id))
            .execute()
        )
        if not response.data:
            return None
        return Email(**response.data[0])
