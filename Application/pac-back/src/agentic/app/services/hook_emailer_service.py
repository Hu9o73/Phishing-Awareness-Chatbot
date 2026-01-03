from uuid import UUID

from app.agents.hook_emailer_agent import HookEmailerAgent
from app.database.interactors.Agentic.scenarios import AgenticScenariosInteractor
from app.models.base_models import HookEmailGenerationResponse, PublicUserModel
from app.models.enum_models import RoleEnum
from app.services.Base.authentication import AuthenticationService
from fastapi import HTTPException, status
from langfuse.decorators import langfuse_context, observe


class HookEmailerService:
    @staticmethod
    def _get_current_member(token: str) -> PublicUserModel:
        user = AuthenticationService.get_current_user(token)
        if user.role != RoleEnum.MEMBER:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only members can generate hook emails.")
        if user.organization_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User must belong to an organization to generate hook emails.",
            )
        return user

    @staticmethod
    @observe(as_type="trace")
    async def generate_hook_email(token: str, scenario_id: UUID) -> HookEmailGenerationResponse:
        user = HookEmailerService._get_current_member(token)
        scenario = await AgenticScenariosInteractor.get_scenario(user.organization_id, scenario_id)
        if scenario is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scenario not found.")

        agent = HookEmailerAgent()
        drafted = await agent.generate_hook_email(scenario)

        langfuse_context.update_current_observation(name="Method: POST generate-hook-email")
        langfuse_context.update_current_trace(
            name="Hook Email Generation",
            input={"scenario_id": str(scenario_id)},
            user_id=str(user.id) if user.id else None,
            session_id=str(scenario_id),
            output=drafted,
        )

        return HookEmailGenerationResponse(
            subject=drafted.get("subject"),
            body=drafted.get("body") or "<html><body><p></p></body></html>",
        )
