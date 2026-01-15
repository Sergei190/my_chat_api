from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.database import get_async_session
from app.schemas.message import MessageCreate, MessageResponse
from app.services.message_service import MessageService
from app.dependencies import get_message_service

router = APIRouter(prefix="/chats/{chat_id}", tags=["messages"])

logger = logging.getLogger(__name__)


@router.post("/messages/", response_model=MessageResponse, status_code=201)
async def create_message(
    chat_id: int,
    message_data: MessageCreate,
    message_service: MessageService = Depends(get_message_service),
    db: AsyncSession = Depends(get_async_session)
) -> MessageResponse:
    """
    Отправить сообщение в чат.
    """
    try:
        logger.info(f"Sending message to chat {chat_id}: {message_data.text[:20]}...")
        message = await message_service.send_message(chat_id, message_data.text)
        logger.info(f"Message sent successfully: {message.id}")
        return message
    except HTTPException:
        logger.error("HTTPException in create_message")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in create_message: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred")