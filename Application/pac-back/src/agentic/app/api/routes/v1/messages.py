from datetime import datetime

from app.models.base_models import MessageModel
from app.services.messages_service import MessagesService
from fastapi import APIRouter

router = APIRouter()


@router.post("/message", description="Send a message.", response_model=MessageModel)
async def create_message(message: str):
    answer = await MessagesService.send_message(message)

    return MessageModel(
        message=answer,
        created_at=datetime.now()
    )
