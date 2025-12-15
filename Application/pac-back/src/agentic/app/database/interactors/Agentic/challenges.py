from datetime import datetime, timezone
from uuid import UUID

from app.database.client import get_db
from app.models.base_models import Challenge
from app.models.enum_models import ChallengeStatus
from supabase import Client


class AgenticChallengesInteractor:
    @staticmethod
    async def get_challenge(challenge_id: UUID) -> Challenge | None:
        supabase: Client = get_db()
        response = supabase.table("challenges").select("*").eq("id", str(challenge_id)).limit(1).execute()
        if not response.data:
            return None
        return Challenge(**response.data[0])

    @staticmethod
    async def update_challenge(
        challenge_id: UUID, status: ChallengeStatus, score: int | None, last_exchange_id: UUID
    ) -> Challenge | None:
        supabase: Client = get_db()
        update_payload: dict[str, str | int | None] = {
            "status": status.value,
            "last_exchange_id": str(last_exchange_id),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        update_payload["score"] = score if score is not None else None

        response = supabase.table("challenges").update(update_payload).eq("id", str(challenge_id)).execute()
        if not response.data:
            return None
        return Challenge(**response.data[0])
