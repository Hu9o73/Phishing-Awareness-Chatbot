from app.agents.basic_agent import basic_agent


class MessagesService:
    @staticmethod
    async def send_message(user_message: str) -> str:
        return await basic_agent.send_message(user_message)
