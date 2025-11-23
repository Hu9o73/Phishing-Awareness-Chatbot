from __future__ import annotations

from datetime import datetime
from uuid import UUID

from app.database.interactors.Base.org_members import OrgMembersInteractor
from app.database.interactors.Monitoring.challenges import MonitoringChallengesInteractor
from app.database.interactors.Monitoring.exchanges import MonitoringExchangesInteractor
from app.database.interactors.Monitoring.scenarios import MonitoringScenariosInteractor
from app.models.base_models import (
    Challenge,
    ChallengeListResponse,
    ChallengeStatusResponse,
    ChallengeStatusUpdate,
    Email,
    EmailCreate,
    ExchangesResponse,
    PublicUserModel,
    StatusResponse,
)
from app.models.enum_models import ChallengeStatus, ChannelEnum, EmailRole, EmailStatus, RoleEnum
from app.services.Base.authentication import AuthenticationService
from app.services.email_service import (
    extract_challenge_id_from_html,
    get_received_email,
    list_incoming_replies,
    send_email,
)
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

        hook_exchange = await MonitoringExchangesInteractor.get_hook_exchange_for_scenario(scenario_id)
        if hook_exchange is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Hook email not found for scenario."
            )

        challenge = await MonitoringChallengesInteractor.create_challenge(user.id, employee_id, scenario_id)
        challenge_id = str(challenge.id)
        try:
            # Send hook email
            send_email(
                employee.email, hook_exchange.subject, hook_exchange.body, hook_exchange.sender_email, challenge_id
            )
        # TODO: Discuss the need for the double exception
        except HTTPException:
            await MonitoringChallengesInteractor.delete_challenge(challenge.id)
            raise
        except Exception as exc:  # noqa: BLE001
            await MonitoringChallengesInteractor.delete_challenge(challenge.id)
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY, detail="Failed to send hook email."
            ) from exc

        sent_email = await MonitoringExchangesInteractor.create_email_in_db(
            EmailCreate(
                scenario_id=hook_exchange.scenario_id,
                role=EmailRole.AI,
                target_id=employee_id,
                previous_email=hook_exchange.id,
                subject=hook_exchange.subject,
                sender_email=hook_exchange.sender_email,
                language=hook_exchange.language,
                body=hook_exchange.body,
                variables=hook_exchange.variables,
                status=EmailStatus.SENT,
                challenge_id=challenge.id,
            )
        )
        updated_challenge = await MonitoringChallengesInteractor.update_last_exchange_id(challenge.id, sent_email.id)
        # TODO: Handle more gracefully this error, what if we can't update the challenge in the db ? Is it really bad ?
        if updated_challenge is None:
            challenge.last_exchange_id = sent_email.id
            return challenge
        return updated_challenge

    @staticmethod
    async def retrieve_status(token: str, challenge_id: UUID) -> ChallengeStatusResponse:
        challenge = await MonitoringService._get_challenge_for_org(token, challenge_id)
        return ChallengeStatusResponse(status=challenge.status)

    @staticmethod
    async def list_challenges(token: str, status: ChallengeStatus | None = None) -> ChallengeListResponse:
        user = MonitoringService._get_current_member_user(token)
        challenges = await MonitoringChallengesInteractor.list_challenges_for_user(user.id, status)
        return ChallengeListResponse(items=challenges)

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

    @staticmethod
    async def send_all_pending_emails(token: str) -> StatusResponse:
        organization_id = MonitoringService._get_user_organization_id(token)
        user_id = MonitoringService._get_current_member_user(token)
        challenges = await MonitoringChallengesInteractor.list_challenges_for_user(user_id)
        sent_count = 0

        for challenge in challenges:
            target_member = await OrgMembersInteractor.get_member(challenge.employee_id)
            if target_member is None or target_member.organization_id != organization_id:
                # We just skip and ignore the error, do we want that ?
                continue

            pending_emails = await MonitoringExchangesInteractor.list_emails_for_target(
                challenge.scenario_id, challenge.employee_id, EmailStatus.PENDING, challenge.id
            )
            for email in pending_emails:
                previous_email = None
                if email.previous_email is not None:
                    previous_email = await MonitoringExchangesInteractor.get_email(email.previous_email)

                if previous_email is not None and previous_email.challenge_id is not None:
                    challenge_id = str(previous_email.challenge_id)
                else:
                    challenge_id = str(challenge.id)

                recipient_email = target_member.email
                if previous_email is not None and previous_email.role == EmailRole.USER and previous_email.sender_email:
                    recipient_email = previous_email.sender_email

                subject = email.subject
                if subject is None and previous_email is not None and previous_email.subject:
                    subject = f"Re: {previous_email.subject}"

                send_email(recipient_email, subject, email.body, email.sender_email, challenge_id)
                # Update status (and eventually challenge_id)
                await MonitoringExchangesInteractor.update_email_send_info(email.id, UUID(challenge_id), EmailStatus.SENT)
                sent_count += 1

        return StatusResponse(status="ok", message=f"Sent {sent_count} pending emails.")


    @staticmethod
    async def retrieve_answers(token: str) -> StatusResponse:
        organization_id = MonitoringService._get_user_organization_id(token)
        stored_count = 0
        after: str | None = None
        latest_received = await MonitoringExchangesInteractor.get_latest_received_email()
        last_received_uuid = latest_received.id if latest_received else None
        reached_known_email = False

        while True:
            page = list_incoming_replies(after=after)
            replies: list[dict] = page.get("data", None)
            has_more = page.get("has_more", False)

            if not replies:
                break

            for reply in replies:
                email_id = reply.get("id", None)
                inbound_uuid = UUID(str(email_id))
                if last_received_uuid is not None and inbound_uuid == last_received_uuid:
                    reached_known_email = True
                    break

                detailed_reply = get_received_email(email_id=email_id)

                challenge_id = extract_challenge_id_from_html(detailed_reply.get("html", None))
                challenge_id = str(challenge_id).strip() if challenge_id else None

                created_at_raw = detailed_reply.get("created_at", None)
                try:
                    created_at_dt = datetime.fromisoformat(str(created_at_raw).replace("Z", "+00:00"))
                except ValueError:
                    created_at_dt = None

                if challenge_id and created_at_dt:
                    previous_email = await MonitoringExchangesInteractor.get_latest_by_challenge_before(
                        UUID(challenge_id), created_at_dt
                    )
                else:
                    previous_email = None

                if previous_email is None:
                    # Skip, not an answer
                    continue

                scenario_id = previous_email.scenario_id

                scenario = await MonitoringScenariosInteractor.get_scenario(organization_id, scenario_id)
                if scenario is None:
                    # Skip, couldn't find scenario the email is binded to
                    continue

                target_id = previous_email.target_id

                if target_id is not None:
                    target_member = await OrgMembersInteractor.get_member(target_id)
                    if target_member is None or target_member.organization_id != organization_id:
                        # Skip, wrong member
                        continue

                sender_email = detailed_reply.get("from", "")
                body = ""
                body = detailed_reply.get("html") or detailed_reply.get("text") or ""

                new_email = EmailCreate(
                    id=inbound_uuid,
                    scenario_id=scenario_id,
                    role=EmailRole.USER,
                    target_id=target_id,
                    previous_email=previous_email.id,
                    subject=detailed_reply.get("subject", None),
                    sender_email=sender_email or "",
                    language=previous_email.language or "en", # This might be changed but for now set to en
                    body=body,
                    variables=None,
                    status=EmailStatus.RECIEVED,
                    challenge_id=previous_email.challenge_id,
                )

                await MonitoringExchangesInteractor.create_email_in_db(new_email)
                stored_count += 1

            if reached_known_email:
                break

            if not has_more:
                break
            last_id = replies[-1].get("id", None)
            if last_id is None:
                break
            after = last_id

        return StatusResponse(status="ok", message=f"Found {stored_count} received emails.")

    @staticmethod
    async def update_challenge_status(
        token: str, challenge_id: UUID, challenge_update: ChallengeStatusUpdate
    ) -> Challenge:
        challenge = await MonitoringService._get_challenge_for_org(token, challenge_id)
        if challenge_update.status not in (ChallengeStatus.SUCCESS, ChallengeStatus.FAILURE):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Challenge status can only be set to SUCCESS or FAILURE.",
            )

        raw_score = challenge_update.score if challenge_update.score is not None else 0
        if isinstance(raw_score, float) and not raw_score.is_integer():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Score must be an integer value.",
            )
        try:
            score = int(raw_score)
        except (TypeError, ValueError) as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Score must be an integer value.",
            ) from exc
        if score < 0 or score > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Score must be between 0 and 100.",
            )
        updated = await MonitoringChallengesInteractor.update_challenge_status(
            challenge.id, challenge_update.status, score
        )
        if updated is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Challenge not found.",
            )
        return updated

    @staticmethod
    async def delete_challenge(token: str, challenge_id: UUID) -> StatusResponse:
        challenge = await MonitoringService._get_challenge_for_org(token, challenge_id)
        if challenge.status not in (ChallengeStatus.SUCCESS, ChallengeStatus.FAILURE):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only completed challenges can be deleted.",
            )

        deleted = await MonitoringChallengesInteractor.delete_challenge(challenge.id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Challenge not found.",
            )
        return StatusResponse(status="ok", message=f"Challenge {challenge_id} deleted successfully.")
