import json

from app.agents.agent_base import AgentBase
from app.agents.email_agentic_flow import EmailWriterAgent
from app.models.base_models import Scenario
from langchain_core.messages import HumanMessage, SystemMessage
from langfuse.decorators import langfuse_context, observe


class HookEmailerAgent(AgentBase):
    def _get_available_tools(self) -> list[callable]:
        return []

    @staticmethod
    def _fallback_subject() -> str:
        return "Quick request"

    @staticmethod
    def _parse_response(content: str) -> dict[str, str | None]:
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
            body = parsed.get("body") or parsed.get("html")
        except json.JSONDecodeError:
            body = cleaned

        subject = subject or HookEmailerAgent._fallback_subject()
        body = EmailWriterAgent._ensure_html_body(body or "")
        return {"subject": subject, "body": body}

    @observe(as_type="generation")
    async def generate_hook_email(self, scenario: Scenario) -> dict[str, str | None]:
        llm = await self._create_openai_llm()
        messages = [
            SystemMessage(
                content=(
                    "You are the hook email agent for a phishing awareness challenge. "
                    "Craft the very first email (hook) sent to the participant. "
                    "The scenario is the source of truth; stay aligned with its goal. "
                    "Write as the phishing actor within the scenario, never as the platform user. "
                    "Return JSON with keys 'subject' and 'body'. "
                    "The 'body' must be a valid HTML string using simple tags like <p>, <br>, <ul>, <ol>, <strong>. "
                    "You may include {{first_name}} and {{last_name}} placeholders for greeting only. "
                    "Do not include any other placeholders or variables. "
                    "Do not include markdown or code fences."
                )
            ),
            HumanMessage(
                content=(
                    f"Scenario name: {scenario.name}\n"
                    f"Scenario complexity: {scenario.complexity}\n"
                    f"Scenario system prompt:\n{scenario.system_prompt}\n"
                    f"Scenario misc info:\n{scenario.misc_info}\n"
                )
            ),
        ]

        llm_response = await self._llm_call_with_tools(llm, messages)
        langfuse_context.update_current_observation(name="Agent: Hook Emailer")
        content = llm_response if isinstance(llm_response, str) else llm_response.content
        return self._parse_response(content)


hook_emailer_agent = HookEmailerAgent()
