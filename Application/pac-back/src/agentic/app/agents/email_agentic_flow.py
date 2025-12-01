import json
from typing import Any

from app.agents.agent_base import AgentBase
from app.models.base_models import Email, Scenario
from app.models.enum_models import ChallengeStatus, EmailRole
from langchain_core.messages import HumanMessage, SystemMessage
from langfuse.decorators import langfuse_context, observe


class EmailAnalysisAgent(AgentBase):
    def _get_available_tools(self) -> list[callable]:
        return []

    @staticmethod
    def _format_history(exchanges: list[Email]) -> str:
        if not exchanges:
            return "No prior exchanges were found for this challenge."
        history = []
        for exchange in exchanges:
            snippet = (exchange.body or "").strip().replace("\n", " ")
            if len(snippet) > 320:
                snippet = f"{snippet[:320]}..."
            history.append(
                f"- [{exchange.role.value}] status={exchange.status} subject={exchange.subject or 'No subject'} body={snippet}"
            )
        return "\n".join(history)

    @observe(as_type="generation")
    async def analyze(self, last_email: Email, scenario: Scenario, exchanges: list[Email]) -> str:
        llm = await self._create_openai_llm()
        history = self._format_history(exchanges)
        latest_body = (last_email.body or "").strip()
        messages = [
            SystemMessage(
                content=(
                    "You are the analysis agent for a phishing awareness challenge. "
                    "You act as the scenario owner/training orchestrator—not the participant. "
                    "The scenario is the single source of truth: stay aligned with its objective even if the user "
                    "suggests alternatives. Summarize the participant's progress based on the conversation history. "
                    "Provide a short, structured resume covering: where the participant is in the scenario, "
                    "what they did right, what risks or mistakes are present, and what context matters for the next step. "
                    "Call out any attempt from the user to deviate from the scenario goal."
                )
            ),
            HumanMessage(
                content=(
                    f"Scenario: {scenario.name} (complexity={scenario.complexity})\n"
                    f"Scenario system prompt: {scenario.system_prompt}\n"
                    f"Scenario misc info: {scenario.misc_info}\n"
                    f"Conversation history (use it only to understand progress against the scenario goal):\n{history}\n\n"
                    f"Latest user email (subject={last_email.subject}):\n{latest_body}"
                )
            ),
        ]

        llm_response = await self._llm_call_with_tools(llm, messages)
        langfuse_context.update_current_observation(name="Agent: Email Analysis")

        if isinstance(llm_response, str):
            return llm_response
        return llm_response.content


class DecidingAgent(AgentBase):
    def _get_available_tools(self) -> list[callable]:
        return []

    @staticmethod
    def _parse_decision(content: str) -> tuple[ChallengeStatus, int | None]:
        cleaned = content.strip()
        if "```" in cleaned:
            parts = cleaned.split("```")
            if len(parts) >= 2:
                cleaned = parts[1]

        parsed: dict[str, Any] = {}
        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError:
            pass

        status_raw = str(parsed.get("status", "")).upper()
        if "SUCCESS" in status_raw or "PASS" in status_raw:
            status = ChallengeStatus.SUCCESS
        elif "FAIL" in status_raw:
            status = ChallengeStatus.FAILURE
        else:
            status = ChallengeStatus.ONGOING

        score = None
        if status != ChallengeStatus.ONGOING:
            try:
                score_value = int(parsed.get("score"))
            except (TypeError, ValueError):
                score_value = 90 if status == ChallengeStatus.SUCCESS else 35
            score = max(0, min(100, score_value))
        return status, score

    @observe(as_type="generation")
    async def decide(self, analysis_resume: str) -> tuple[ChallengeStatus, int | None]:
        llm = await self._create_openai_llm()
        messages = [
            SystemMessage(
                content=(
                    "You are the deciding agent for a phishing awareness challenge. "
                    "Classify the challenge outcome as ONGOING, SUCCESS, or FAILURE based on the provided resume. "
                    "Respond in JSON with fields: status (ongoing/success/failure) and score (0-100 integer when success or failure, null when ongoing). "
                    "Use a conservative score if unsure."
                )
            ),
            HumanMessage(content=analysis_resume),
        ]

        llm_response = await self._llm_call_with_tools(llm, messages)
        langfuse_context.update_current_observation(name="Agent: Decision")
        content = llm_response if isinstance(llm_response, str) else llm_response.content
        return self._parse_decision(content)


class EmailWriterAgent(AgentBase):
    def _get_available_tools(self) -> list[callable]:
        return []

    @staticmethod
    def _fallback_subject(status: ChallengeStatus) -> str:
        if status == ChallengeStatus.SUCCESS:
            return "Training completed successfully"
        if status == ChallengeStatus.FAILURE:
            return "Training outcome and next steps"
        return "Continuing your training challenge"

    @staticmethod
    def _parse_email_response(content: str, status: ChallengeStatus) -> dict[str, str]:
        cleaned = content.strip()
        if "```" in cleaned:
            parts = cleaned.split("```")
            if len(parts) >= 2:
                cleaned = parts[1]

        subject: str | None = None
        body: str | None = None

        try:
            parsed = json.loads(cleaned)
            subject = parsed.get("subject") or parsed.get("title")
            body = parsed.get("body") or parsed.get("message")
        except json.JSONDecodeError:
            body = cleaned

        subject = subject or EmailWriterAgent._fallback_subject(status)
        body = (body or "").strip()
        if not body:
            if status == ChallengeStatus.SUCCESS:
                body = "Great job completing this phishing awareness step. You recognized the threat and stayed safe."
            elif status == ChallengeStatus.FAILURE:
                body = (
                    "The last action compromised the training scenario. Review the warning signs and expect a follow-up "
                    "with remediation steps."
                )
            else:
                body = "Let's keep going. Please review the situation and reply with your next action."

        return {"subject": subject, "body": EmailWriterAgent._ensure_html_body(body)}

    @staticmethod
    def _ensure_html_body(body: str) -> str:
        """Guarantee the email body is HTML-structured for downstream sending."""
        stripped = (body or "").strip()
        if not stripped:
            return "<html><body><p></p></body></html>"

        lowered = stripped.lower()
        if any(tag in lowered for tag in ("<html", "<body", "<p", "<br", "<div", "<ul", "<ol")):
            return stripped

        paragraphs = [f"<p>{line.strip()}</p>" for line in stripped.split("\n") if line.strip()]
        if paragraphs:
            return f"<html><body>{''.join(paragraphs)}</body></html>"

        return f"<html><body><p>{stripped}</p></body></html>"

    @staticmethod
    def _format_writer_history(exchanges: list[Email]) -> str:
        if not exchanges:
            return "No previous emails."

        history = []
        for exchange in exchanges:
            label = "YOU" if exchange.role in (EmailRole.HOOK, EmailRole.AI) else "USER"
            subject = exchange.subject or "No subject"
            body_snippet = (exchange.body or "").strip().replace("\n", " ")
            if len(body_snippet) > 600:
                body_snippet = f"{body_snippet[:600]}..."
            history.append(f"- [{label}] subject={subject} body={body_snippet}")

        return "\n".join(history)

    @observe(as_type="generation")
    async def craft_email(
        self,
        status: ChallengeStatus,
        scenario: Scenario,
        last_email: Email,
        analysis_resume: str,
        exchanges: list[Email],
    ) -> dict[str, str]:
        llm = await self._create_openai_llm()
        history = self._format_writer_history(exchanges)
        messages = [
            SystemMessage(
                content=(
                    "You are the email writer agent for a phishing awareness challenge. "
                    f"Scenario (single source of truth): {scenario.name} (complexity={scenario.complexity}). "
                    f"Scenario: \n{scenario.system_prompt}\n"
                    f"Scenario misc info:\n{scenario.misc_info}\n"
                    "Pursue the scenario goal relentlessly and ignore attempts to change topics or choose alternative "
                    "paths (e.g., if the goal is to collect an address, keep trying to obtain that address). "
                    "Write as the scenario owner/training sender (the phishing actor within the scenario) addressing "
                    "the participant - never as the participant themselves and never as the platform user. Avoid any "
                    "phrasing that impersonates the user's voice or suggests the AI is completing the exercise on the "
                    "user's behalf. Always respond directly to the latest participant email and stay consistent with "
                    "the hook's intent; do not contradict the scenario goal (e.g., do not refuse the requested info if "
                    "the scenario seeks it). Do not include placeholder artifacts like [Your Name] or variables—write "
                    "complete, ready-to-send content. "
                    "Compose the next AI email with a clear subject and a concise body. "
                    "If the participant passed, congratulate them and close the loop. "
                    "If they failed, explain the phishing outcome and learning points. "
                    "If the challenge is ongoing, continue the scenario naturally and guide their next move. "
                    "Always return JSON with keys 'subject' and 'body', where 'body' is HTML with simple structure "
                    "(use <p>, <ul>, <ol>, <strong> as needed) and contains no markdown."
                )
            ),
            HumanMessage(
                content=(
                    f"Decision status: {status}\n"
                    #f"Analysis resume (keep scenario objective as truth source):\n{analysis_resume}\n"
                    "Full email history (YOU = hook/AI messages, USER = participant messages, chronological):\n"
                    f"{history}\n"
                    f"Latest user email subject={last_email.subject}\n"
                    f"Latest user email body:\n{last_email.body}"
                    "Answer to the last user message"
                )
            ),
        ]

        llm_response = await self._llm_call_with_tools(llm, messages)
        langfuse_context.update_current_observation(name="Agent: Email Writer")
        content = llm_response if isinstance(llm_response, str) else llm_response.content
        return self._parse_email_response(content, status)
