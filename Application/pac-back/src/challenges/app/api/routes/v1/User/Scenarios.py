from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.models.base_models import Scenario, ScenarioCreate, ScenarioExport, ScenarioUpdate, StatusResponse
from app.services.User.scenarios import UserScenarioService

router = APIRouter()
security = HTTPBearer()


@router.post("/scenarios", response_model=Scenario, status_code=status.HTTP_201_CREATED)
async def create_scenario(
    scenario: ScenarioCreate, credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Scenario:
    token = credentials.credentials
    return await UserScenarioService.create_scenario(token, scenario)


@router.put("/scenarios", response_model=Scenario)
async def update_scenario(
    scenario_update: ScenarioUpdate,
    scenario_id: UUID = Query(..., description="Identifier of the scenario to update."),
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Scenario:
    token = credentials.credentials
    return await UserScenarioService.update_scenario(token, scenario_id, scenario_update)


@router.delete("/scenarios", response_model=StatusResponse)
async def delete_scenario(
    scenario_id: UUID = Query(..., description="Identifier of the scenario to delete."),
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> StatusResponse:
    token = credentials.credentials
    return await UserScenarioService.delete_scenario(token, scenario_id)


@router.get("/scenarios/export", response_model=ScenarioExport)
async def export_scenario(
    scenario_id: UUID = Query(..., description="Identifier of the scenario to export."),
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> ScenarioExport:
    token = credentials.credentials
    return await UserScenarioService.export_scenario(token, scenario_id)


@router.post("/scenarios/import", response_model=Scenario, status_code=status.HTTP_201_CREATED)
async def import_scenario(
    scenario_data: ScenarioExport, credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Scenario:
    token = credentials.credentials
    return await UserScenarioService.import_scenario(token, scenario_data)
