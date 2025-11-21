from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from app.database.client import get_db
from app.models.base_models import Challenge
from app.models.enum_models import ChallengeStatus, ChannelEnum
from supabase import Client


class MonitoringChallengesInteractor:
    @staticmethod
    async def create_challenge(user_id: UUID, employee_id: UUID, scenario_id: UUID) -> Challenge:
        supabase: Client = get_db()
        payload: dict[str, Any] = {
            "user_id": str(user_id),
            "employee_id": str(employee_id),
            "scenario_id": str(scenario_id),
            "channel": ChannelEnum.EMAIL.value,
            "status": ChallengeStatus.ONGOING.value,
            "score": None,
            "last_exchange_id": None,
        }
        response = supabase.table("challenges").insert(payload).execute()
        if not response.data:
            raise ValueError("Failed to create challenge")
        return Challenge(**response.data[0])

    @staticmethod
    async def get_challenge(challenge_id: UUID) -> Challenge | None:
        supabase: Client = get_db()
        response = supabase.table("challenges").select("*").eq("id", str(challenge_id)).limit(1).execute()
        if not response.data:
            return None
        return Challenge(**response.data[0])

    @staticmethod
    async def list_challenges_for_user(user_id: UUID, status: ChallengeStatus | None = None) -> list[Challenge]:
        supabase: Client = get_db()
        query = supabase.table("challenges").select("*").eq("user_id", str(user_id))
        if status is not None:
            query = query.eq("status", status.value)
        response = query.execute()
        if not response.data:
            return []
        return [Challenge(**entry) for entry in response.data]

    @staticmethod
    async def update_last_exchange_id(challenge_id: UUID, exchange_id: UUID) -> Challenge | None:
        supabase: Client = get_db()
        response = (
            supabase.table("challenges")
            .update(
                {
                    "last_exchange_id": str(exchange_id),
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                }
            )
            .eq("id", str(challenge_id))
            .execute()
        )
        if not response.data:
            return None
        return Challenge(**response.data[0])
