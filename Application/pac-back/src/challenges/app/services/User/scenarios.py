from uuid import UUID

from fastapi import HTTPException, status

from app.database.interactors.User.scenarios import UserScenariosInteractor
from app.models.base_models import (
    Scenario,
    ScenarioCreate,
    ScenarioExport,
    ScenarioUpdate,
    StatusResponse,
)
from app.services.Base.authentication import AuthenticationService


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
    async def create_scenario(token: str, scenario: ScenarioCreate) -> Scenario:
        organization_id = UserScenarioService._get_user_organization_id(token)
        return await UserScenariosInteractor.create_scenario(organization_id, scenario)

    @staticmethod
    async def update_scenario(token: str, scenario_id: UUID, scenario_update: ScenarioUpdate) -> Scenario:
        organization_id = UserScenarioService._get_user_organization_id(token)
        existing_scenario = await UserScenariosInteractor.get_scenario(organization_id, scenario_id)
        if existing_scenario is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scenario not found.",
            )

        update_payload = scenario_update.model_dump(exclude_unset=True, exclude_none=True)
        if not update_payload:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided to update the scenario.",
            )

        return await UserScenariosInteractor.update_scenario(organization_id, scenario_id, scenario_update)

    @staticmethod
    async def delete_scenario(token: str, scenario_id: UUID) -> StatusResponse:
        organization_id = UserScenarioService._get_user_organization_id(token)
        scenario = await UserScenariosInteractor.get_scenario(organization_id, scenario_id)
        if scenario is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scenario not found.",
            )

        await UserScenariosInteractor.delete_scenario(organization_id, scenario_id)
        return StatusResponse(status="ok", message=f"Scenario {scenario_id} deleted successfully.")

    @staticmethod
    async def export_scenario(token: str, scenario_id: UUID) -> ScenarioExport:
        organization_id = UserScenarioService._get_user_organization_id(token)
        scenario = await UserScenariosInteractor.get_scenario(organization_id, scenario_id)
        if scenario is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scenario not found.",
            )

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
