import os
from uuid import UUID

from app.agents.email_agentic_flow import DecidingAgent, EmailAnalysisAgent, EmailWriterAgent
from app.database.interactors.Agentic.challenges import AgenticChallengesInteractor
from app.database.interactors.Agentic.emails import AgenticEmailsInteractor
from app.database.interactors.Agentic.scenarios import AgenticScenariosInteractor
from app.models.base_models import (
    AgenticFlowResponse,
    Challenge,
    Email,
    EmailCreate,
    PublicUserModel,
    Scenario,
    StatusResponse,
)
from app.models.enum_models import ChallengeStatus, ChannelEnum, EmailRole, EmailStatus, RoleEnum
from app.services.Base.authentication import AuthenticationService
from app.services.Base.monitoring import MonitoringServiceClient
from fastapi import HTTPException, status
from langfuse.decorators import langfuse_context, observe


class AgenticFlowService:
    @staticmethod
    def _is_super_clock_token(super_clock_token: str | None) -> bool:
        expected = os.getenv("SUPER_CLOCK_TOKEN")
        return bool(expected and super_clock_token == expected)

    @staticmethod
    def _get_current_member(token: str) -> PublicUserModel:
        user = AuthenticationService.get_current_user(token)
        if user.role != RoleEnum.MEMBER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only members can trigger the agentic flow.",
            )
        if user.organization_id is None or user.id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User must belong to an organization to run the agentic flow.",
            )
        return user

    @staticmethod
    async def _get_challenge_context_super(challenge_id: UUID):
        challenge = await AgenticChallengesInteractor.get_challenge(challenge_id)
        if challenge is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Challenge not found.")
        if challenge.channel != ChannelEnum.EMAIL:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported channel for agentic flow.",
            )
        if challenge.status != ChallengeStatus.ONGOING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Challenge must be ongoing to run the agentic flow.",
            )
        if challenge.last_exchange_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Challenge has no exchanges yet.",
            )

        scenario = await AgenticScenariosInteractor.get_scenario_by_id(challenge.scenario_id)
        if scenario is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scenario not found.")

        last_email = await AgenticEmailsInteractor.get_email(challenge.last_exchange_id)
        if last_email is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Last email not found.")
        if last_email.status != EmailStatus.RECIEVED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Latest email must be marked as received.",
            )
        if last_email.role != EmailRole.USER:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Latest email must come from the user.",
            )

        previous_email = None
        if last_email.previous_email is not None:
            previous_email = await AgenticEmailsInteractor.get_email(last_email.previous_email)

        return challenge, scenario, last_email, previous_email

    @staticmethod
    async def _get_challenge_context(token: str, challenge_id: UUID):
        user = AgenticFlowService._get_current_member(token)
        challenge = await AgenticChallengesInteractor.get_challenge(challenge_id)
        if challenge is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Challenge not found.")
        if challenge.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Users can only trigger flows for their own challenges.",
            )
        if challenge.channel != ChannelEnum.EMAIL:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported channel for agentic flow.",
            )
        if challenge.status != ChallengeStatus.ONGOING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Challenge must be ongoing to run the agentic flow.",
            )

        scenario = await AgenticScenariosInteractor.get_scenario(user.organization_id, challenge.scenario_id)
        if scenario is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scenario not found.")

        if challenge.last_exchange_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Challenge has no exchanges yet.",
            )

        last_email = await AgenticEmailsInteractor.get_email(challenge.last_exchange_id)
        if last_email is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Last email not found.")
        if last_email.status != EmailStatus.RECIEVED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Latest email must be marked as received.",
            )
        if last_email.role != EmailRole.USER:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Latest email must come from the user.",
            )

        previous_email = None
        if last_email.previous_email is not None:
            previous_email = await AgenticEmailsInteractor.get_email(last_email.previous_email)

        return challenge, scenario, last_email, previous_email, user

    @staticmethod
    async def _build_exchanges_from_last_email(last_email: Email) -> list[Email]:
        exchanges: list[Email] = []
        current = last_email
        while current is not None:
            exchanges.append(current)
            if current.role == EmailRole.HOOK or current.previous_email is None:
                break
            current = await AgenticEmailsInteractor.get_email(current.previous_email)
        exchanges.reverse()
        return exchanges

    @staticmethod
    async def _run_email_flow_from_context(
        challenge: Challenge,
        scenario: Scenario,
        last_email: Email,
        previous_email: Email | None,
        exchanges: list[Email],
        user_id: UUID,
    ) -> AgenticFlowResponse:
        langfuse_context.update_current_trace(
            name="Email Agentic Flow",
            input={"challenge_id": str(challenge.id), "last_email_id": str(last_email.id)},
            user_id=str(user_id),
            session_id=str(challenge.id),
        )

        analysis_agent = EmailAnalysisAgent()
        analysis_resume = await analysis_agent.analyze(last_email, scenario, exchanges)

        decision_agent = DecidingAgent()
        decision_status, decision_score = await decision_agent.decide(analysis_resume)

        writer_agent = EmailWriterAgent()
        drafted_email = await writer_agent.craft_email(
            decision_status, scenario, last_email, analysis_resume, exchanges or []
        )

        subject = drafted_email.get("subject") or (previous_email.subject if previous_email else last_email.subject)
        body = drafted_email.get("body") or "Thank you for your response. Expect further instructions soon."
        sender_email = (
            previous_email.sender_email
            if previous_email is not None and previous_email.sender_email
            else last_email.sender_email
        )

        email_payload = EmailCreate(
            scenario_id=last_email.scenario_id,
            role=EmailRole.AI,
            sender_email=sender_email,
            language=last_email.language,
            target_id=last_email.target_id,
            previous_email=last_email.id,
            subject=subject,
            body=body,
            variables=None,
            status=EmailStatus.PENDING,
            challenge_id=challenge.id,
        )
        new_email = await AgenticEmailsInteractor.create_email_in_db(email_payload)

        updated_challenge = await AgenticChallengesInteractor.update_challenge(
            challenge.id, decision_status, decision_score, new_email.id
        )
        effective_status = updated_challenge.status if updated_challenge else decision_status
        effective_score = decision_score if effective_status != ChallengeStatus.ONGOING else None
        if updated_challenge is not None and updated_challenge.score is not None:
            try:
                effective_score = int(updated_challenge.score)
            except (TypeError, ValueError):
                effective_score = decision_score if effective_status != ChallengeStatus.ONGOING else None

        langfuse_context.update_current_observation(name="Method: POST email-agentic-flow")
        langfuse_context.update_current_trace(
            output={
                "challenge_status": effective_status.value
                if isinstance(effective_status, ChallengeStatus)
                else str(effective_status),
                "email_id": str(new_email.id),
            }
        )

        return AgenticFlowResponse(
            email_id=new_email.id,
            subject=new_email.subject,
            body=new_email.body,
            challenge_status=effective_status,
            score=effective_score,
        )

    @staticmethod
    @observe(as_type="trace")
    async def run_email_flow(token: str, challenge_id: UUID) -> AgenticFlowResponse:
        challenge, scenario, last_email, previous_email, user = await AgenticFlowService._get_challenge_context(
            token, challenge_id
        )
        exchanges = MonitoringServiceClient.get_exchanges(token, challenge.id)
        return await AgenticFlowService._run_email_flow_from_context(
            challenge, scenario, last_email, previous_email, exchanges, user.id
        )

    @staticmethod
    @observe(as_type="trace")
    async def run_email_flow_for_super_token(challenge_id: UUID) -> AgenticFlowResponse:
        challenge, scenario, last_email, previous_email = await AgenticFlowService._get_challenge_context_super(
            challenge_id
        )
        exchanges = await AgenticFlowService._build_exchanges_from_last_email(last_email)
        return await AgenticFlowService._run_email_flow_from_context(
            challenge, scenario, last_email, previous_email, exchanges, challenge.user_id
        )

    @staticmethod
    async def run_pending_email_flows(super_clock_token: str | None) -> StatusResponse:
        if not AgenticFlowService._is_super_clock_token(super_clock_token):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid super clock token.")

        challenges = await AgenticChallengesInteractor.list_challenges_by_status(ChallengeStatus.ONGOING)
        generated_count = 0

        for challenge in challenges:
            if challenge.last_exchange_id is None:
                continue
            try:
                await AgenticFlowService.run_email_flow_for_super_token(challenge.id)
                generated_count += 1
            except HTTPException:
                continue

        return StatusResponse(status="ok", message=f"Generated {generated_count} AI responses.")
