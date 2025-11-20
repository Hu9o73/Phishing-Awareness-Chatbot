from __future__ import annotations

from uuid import UUID

from app.database.interactors.Base.org_members import OrgMembersInteractor
from app.database.interactors.Monitoring.challenges import MonitoringChallengesInteractor
from app.database.interactors.Monitoring.exchanges import MonitoringExchangesInteractor
from app.database.interactors.Monitoring.scenarios import MonitoringScenariosInteractor
from app.models.base_models import Challenge, ChallengeStatusResponse, Email, ExchangesResponse, PublicUserModel
from app.models.enum_models import ChannelEnum, EmailRole, RoleEnum
from app.services.Base.authentication import AuthenticationService
from app.services.email_service import send_email
from fastapi import HTTPException, status


class MonitoringService:
    @staticmethod
    def _get_user_organization_id(token: str):
        user = AuthenticationService.get_current_user(token)
        if user.organization_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User must belong to an organization to start a challenge.",
            )
        return user.organization_id

    @staticmethod
    async def _get_challenge_for_org(token: str, challenge_id: UUID) -> Challenge:
        organization_id = MonitoringService._get_user_organization_id(token)

        challenge = await MonitoringChallengesInteractor.get_challenge(challenge_id)
        if challenge is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Challenge not found.")

        scenario = await MonitoringScenariosInteractor.get_scenario(organization_id, challenge.scenario_id)
        if scenario is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scenario not found.")

        return challenge

    @staticmethod
    def _get_current_member_user(token: str) -> PublicUserModel:
        user = AuthenticationService.get_current_user(token)

        if user.role != RoleEnum.MEMBER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only members can start a challenge.",
            )

        if user.organization_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User must belong to an organization to start a challenge.",
            )
        if user.id is None:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Invalid user data received from authentication service.",
            )

        return user

    @staticmethod
    async def start_challenge(token: str, employee_id: UUID, scenario_id: UUID) -> Challenge:
        user = MonitoringService._get_current_member_user(token)
        scenario = await MonitoringScenariosInteractor.get_scenario(user.organization_id, scenario_id)
        if scenario is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scenario not found.")

        employee = await OrgMembersInteractor.get_member(employee_id)
        if employee is None or employee.organization_id != user.organization_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found.")

        challenge = await MonitoringChallengesInteractor.create_challenge(user.id, employee_id, scenario_id)

        send_email(employee.email, f"Start phishing awareness challenge for scenario {scenario.name}")

        hook_exchange = await MonitoringExchangesInteractor.get_hook_exchange_for_scenario(scenario_id)
        if hook_exchange is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Hook email not found for scenario."
            )
        updated_challenge = await MonitoringChallengesInteractor.update_last_exchange_id(
            challenge.id, hook_exchange.id
        )
        if updated_challenge is None:
            challenge.last_exchange_id = hook_exchange.id
            return challenge
        return updated_challenge

    @staticmethod
    async def retrieve_status(token: str, challenge_id: UUID) -> ChallengeStatusResponse:
        challenge = await MonitoringService._get_challenge_for_org(token, challenge_id)
        return ChallengeStatusResponse(status=challenge.status)

    @staticmethod
    async def get_exchanges(token: str, challenge_id: UUID) -> ExchangesResponse:
        challenge = await MonitoringService._get_challenge_for_org(token, challenge_id)
        if challenge.channel != ChannelEnum.EMAIL:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported channel for exchanges.",
            )
        if challenge.last_exchange_id is None:
            return ExchangesResponse(exchanges=[])

        exchanges: list[Email] = []
        current = await MonitoringExchangesInteractor.get_exchange(challenge.last_exchange_id)
        if current is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exchange not found.")

        while current is not None:
            exchanges.append(current)
            if current.role == EmailRole.HOOK or current.previous_email is None:
                break
            current = await MonitoringExchangesInteractor.get_exchange(current.previous_email)

        exchanges.reverse()
        return ExchangesResponse(exchanges=exchanges)
