from uuid import UUID

from app.database.interactors.User.emails import UserEmailsInteractor
from app.database.interactors.User.scenarios import UserScenariosInteractor
from app.models.base_models import (
    Email,
    HookEmailCreate,
    HookEmailUpdate,
    Scenario,
    ScenarioCreate,
    ScenarioExport,
    ScenarioListResponse,
    ScenarioUpdate,
    StatusResponse,
)
from app.services.Base.agentic import AgenticServiceClient
from app.services.Base.authentication import AuthenticationService
from fastapi import HTTPException, status


class UserScenarioService:
    @staticmethod
    def _get_user_organization_id(token: str) -> UUID:
        user = AuthenticationService.get_current_user(token)
        if user.organization_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User must belong to an organization to manage scenarios.",
            )
        return user.organization_id

    @staticmethod
    async def _get_owned_scenario(token: str, scenario_id: UUID) -> Scenario:
        organization_id = UserScenarioService._get_user_organization_id(token)
        scenario = await UserScenariosInteractor.get_scenario(organization_id, scenario_id)
        if scenario is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scenario not found.",
            )
        return scenario

    @staticmethod
    async def create_scenario(token: str, scenario: ScenarioCreate) -> Scenario:
        organization_id = UserScenarioService._get_user_organization_id(token)
        created = await UserScenariosInteractor.create_scenario(organization_id, scenario)
        await UserScenarioService._ensure_hook_email(token, created)
        return created

    @staticmethod
    async def list_scenarios(token: str, scenario_id: UUID | None = None) -> ScenarioListResponse:
        organization_id = UserScenarioService._get_user_organization_id(token)
        if scenario_id is not None:
            scenario = await UserScenarioService._get_owned_scenario(token, scenario_id)
            return ScenarioListResponse(items=[scenario])

        scenarios = await UserScenariosInteractor.list_scenarios(organization_id)
        return ScenarioListResponse(items=scenarios)

    @staticmethod
    async def update_scenario(token: str, scenario_id: UUID, scenario_update: ScenarioUpdate) -> Scenario:
        scenario = await UserScenarioService._get_owned_scenario(token, scenario_id)

        update_payload = scenario_update.model_dump(exclude_unset=True, exclude_none=True)
        if not update_payload:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided to update the scenario.",
            )

        updated = await UserScenariosInteractor.update_scenario(scenario.organization_id, scenario_id, scenario_update)
        if updated is not None:
            await UserScenarioService._ensure_hook_email(token, updated)
        return updated

    @staticmethod
    async def delete_scenario(token: str, scenario_id: UUID) -> StatusResponse:
        scenario = await UserScenarioService._get_owned_scenario(token, scenario_id)
        await UserEmailsInteractor.delete_all_for_scenario(scenario_id)
        await UserScenariosInteractor.delete_scenario(scenario.organization_id, scenario_id)
        return StatusResponse(status="ok", message=f"Scenario {scenario_id} deleted successfully.")

    @staticmethod
    async def export_scenario(token: str, scenario_id: UUID) -> ScenarioExport:
        scenario = await UserScenarioService._get_owned_scenario(token, scenario_id)

        return ScenarioExport(
            name=scenario.name,
            complexity=scenario.complexity,
            system_prompt=scenario.system_prompt,
            misc_info=scenario.misc_info or {},
        )

    @staticmethod
    async def import_scenario(token: str, scenario_data: ScenarioExport) -> Scenario:
        organization_id = UserScenarioService._get_user_organization_id(token)
        scenario_create = ScenarioCreate(**scenario_data.model_dump())
        return await UserScenariosInteractor.create_scenario(organization_id, scenario_create)

    @staticmethod
    async def create_hook_email(token: str, scenario_id: UUID, email_data: HookEmailCreate) -> Email:
        existing_email = await UserEmailsInteractor.get_hook_email(scenario_id)
        if existing_email is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A hook email already exists for this scenario.",
            )
        return await UserEmailsInteractor.create_hook_email(scenario_id, email_data)

    @staticmethod
    def _resolve_hook_defaults(scenario: Scenario) -> tuple[str, str]:
        misc_info = scenario.misc_info or {}
        sender_email = misc_info.get("sender_email") or misc_info.get("senderEmail") or "hook@phishward.com"
        language = misc_info.get("language") or misc_info.get("lang") or "en"
        return sender_email, language

    @staticmethod
    async def _ensure_hook_email(token: str, scenario: Scenario) -> None:
        existing_email = await UserEmailsInteractor.get_hook_email(scenario.id)
        if existing_email is not None:
            return
        try:
            await UserScenarioService.generate_hook_email(token, scenario.id)
        except HTTPException:
            return
        except Exception:
            return

    @staticmethod
    async def generate_hook_email(token: str, scenario_id: UUID) -> Email:
        scenario = await UserScenarioService._get_owned_scenario(token, scenario_id)
        existing_email = await UserEmailsInteractor.get_hook_email(scenario_id)
        if existing_email is not None:
            return existing_email

        drafted = AgenticServiceClient.generate_hook_email(token, scenario_id)
        sender_email, language = UserScenarioService._resolve_hook_defaults(scenario)
        email_data = HookEmailCreate(
            subject=drafted.subject,
            sender_email=sender_email,
            language=language,
            body=drafted.body,
            variables=None,
        )
        return await UserEmailsInteractor.create_hook_email(scenario_id, email_data)

    @staticmethod
    async def get_hook_email(token: str, scenario_id: UUID) -> Email:
        _ = await UserScenarioService._get_owned_scenario(token, scenario_id)
        email = await UserEmailsInteractor.get_hook_email(scenario_id)
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Hook email not found for this scenario.",
            )
        return email

    @staticmethod
    async def update_hook_email(token: str, scenario_id: UUID, email_update: HookEmailUpdate) -> Email:
        await UserScenarioService._get_owned_scenario(token, scenario_id)
        update_payload = email_update.model_dump(exclude_unset=True, exclude_none=True)
        if not update_payload:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided to update the hook email.",
            )
        result = await UserEmailsInteractor.update_hook_email(scenario_id, email_update)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Hook email not found for this scenario.",
            )
        return result

    @staticmethod
    async def delete_hook_email(token: str, scenario_id: UUID) -> StatusResponse:
        await UserScenarioService._get_owned_scenario(token, scenario_id)
        email = await UserEmailsInteractor.get_hook_email(scenario_id)
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Hook email not found for this scenario.",
            )
        await UserEmailsInteractor.delete_hook_email(scenario_id)
        return StatusResponse(status="ok", message=f"Hook email for scenario {scenario_id} deleted successfully.")
