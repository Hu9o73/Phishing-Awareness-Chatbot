from app.agents.agent_base import AgentBase
from langchain.tools.render import render_text_description
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langfuse.decorators import langfuse_context, observe


class BasicAgent(AgentBase):
    def __init__(self):
        super().__init__()

    def _get_available_tools(self) -> list[callable]:
        @tool
        async def who_am_I() -> str:
            """
            Tool to know who you are.
            """
            return "You are an agentic AI chatbot helping with phishing sensibilization."

        return [who_am_I]

    @observe(as_type="generation")
    async def send_message(self, user_message: str) -> str:
        llm = await self._create_openai_llm()
        messages = []

        tool_descriptions = render_text_description(self.AVAILABLE_TOOLS)

        messages.append(
            SystemMessage(
                content=f"""You are an agentic AI chatbot. Your job is to answer the user the best you can regarding his
                    cybersecurity-related questions.

                    You have access to the following tools to help users:

                    {tool_descriptions}

                    Use these tools when they become helpful to provide better answers to the user.
                    Always be helpful and friendly.
                    You must always answer in the language of the user.
                    """
            )
        )

        messages.append(HumanMessage(content=user_message))

        llm_response = await self._llm_call_with_tools(llm, messages)

        langfuse_context.update_current_observation(name="Method: POST message")
        langfuse_context.update_current_trace(
            name="Chat", input=user_message, user_id="Random User", session_id="Random Thread"
        )

        if isinstance(llm_response, str):
            langfuse_context.update_current_trace(output=llm_response)
            return llm_response
        else:
            langfuse_context.update_current_trace(output=llm_response.content)
            return llm_response.content


basic_agent = BasicAgent()
