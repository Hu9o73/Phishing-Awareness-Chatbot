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
        return await UserScenariosInteractor.create_scenario(organization_id, scenario)

    @staticmethod
    async def list_scenarios(token: str) -> ScenarioListResponse:
        organization_id = UserScenarioService._get_user_organization_id(token)
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

        return await UserScenariosInteractor.update_scenario(scenario.organization_id, scenario_id, scenario_update)

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
        scenario = await UserScenarioService._get_owned_scenario(token, scenario_id)
        existing_email = await UserEmailsInteractor.get_hook_email(scenario_id)
        if existing_email is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A hook email already exists for this scenario.",
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
