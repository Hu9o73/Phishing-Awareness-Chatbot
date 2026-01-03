import json
from uuid import UUID

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
from app.services.User.scenarios import UserScenarioService
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from fastapi.responses import Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import ValidationError

router = APIRouter()
security = HTTPBearer()


@router.get("/scenarios", response_model=ScenarioListResponse)
async def list_scenarios(
    scenario_id: UUID | None = Query(None, alias="id", description="Return only the matching scenario ID."),
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> ScenarioListResponse:
    token = credentials.credentials
    return await UserScenarioService.list_scenarios(token, scenario_id)


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


@router.post("/scenarios/hook-email", response_model=Email, status_code=status.HTTP_201_CREATED)
async def create_hook_email(
    email: HookEmailCreate,
    scenario_id: UUID = Query(..., description="Identifier of the scenario to attach the hook email to."),
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Email:
    token = credentials.credentials
    return await UserScenarioService.create_hook_email(token, scenario_id, email)


@router.get("/scenarios/hook-email", response_model=Email)
async def get_hook_email(
    scenario_id: UUID = Query(..., description="Identifier of the scenario to fetch the hook email from."),
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Email:
    token = credentials.credentials
    return await UserScenarioService.get_hook_email(token, scenario_id)


@router.put("/scenarios/hook-email", response_model=Email)
async def update_hook_email(
    email_update: HookEmailUpdate,
    scenario_id: UUID = Query(..., description="Identifier of the scenario whose hook email should be updated."),
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Email:
    token = credentials.credentials
    return await UserScenarioService.update_hook_email(token, scenario_id, email_update)


@router.delete("/scenarios/hook-email", response_model=StatusResponse)
async def delete_hook_email(
    scenario_id: UUID = Query(..., description="Identifier of the scenario whose hook email should be deleted."),
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> StatusResponse:
    token = credentials.credentials
    return await UserScenarioService.delete_hook_email(token, scenario_id)


@router.post("/generate-hook-email", response_model=Email)
async def generate_hook_email(
    scenario_id: UUID = Query(..., description="Identifier of the scenario to generate the hook email for."),
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Email:
    token = credentials.credentials
    return await UserScenarioService.generate_hook_email(token, scenario_id)


@router.get("/scenarios/export")
async def export_scenario(
    scenario_id: UUID = Query(..., description="Identifier of the scenario to export."),
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Response:
    token = credentials.credentials
    scenario_data = await UserScenarioService.export_scenario(token, scenario_id)
    file_payload = scenario_data.model_dump()
    file_bytes = json.dumps(file_payload, indent=2).encode("utf-8")
    filename = f"scenario_{scenario_id}.json"
    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
    return Response(content=file_bytes, media_type="application/json", headers=headers)


@router.post("/scenarios/import", response_model=Scenario, status_code=status.HTTP_201_CREATED)
async def import_scenario(
    file: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Scenario:
    token = credentials.credentials
    if file.content_type not in (None, "", "application/json"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file must be a JSON document.",
        )

    try:
        raw_bytes = await file.read()
        payload = json.loads(raw_bytes.decode("utf-8"))
    except UnicodeDecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is not valid UTF-8 encoded JSON.",
        ) from exc
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file contains invalid JSON.",
        ) from exc
    finally:
        await file.close()

    try:
        scenario_data = ScenarioExport(**payload)
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded JSON does not match the expected schema.",
        ) from exc

    return await UserScenarioService.import_scenario(token, scenario_data)
