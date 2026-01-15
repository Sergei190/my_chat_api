from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.database import get_async_session
from app.schemas.chat import ChatCreate, ChatResponse, ChatWithMessagesResponse
from app.services.chat_service import ChatService
from app.dependencies import get_chat_service

router = APIRouter(prefix="/chats", tags=["chats"])

logger = logging.getLogger(__name__)


@router.post("/", response_model=ChatResponse, status_code=201)
async def create_chat(
    chat_data: ChatCreate,
    chat_service: ChatService = Depends(get_chat_service),
    db: AsyncSession = Depends(get_async_session)
) -> ChatResponse:
    """
    Создать новый чат.
    """
    try:
        logger.info(f"Creating chat with title: {chat_data.title}")
        chat = await chat_service.create_chat(chat_data.title)
        logger.info(f"Chat created successfully: {chat.id}")
        return chat
    except HTTPException:
        logger.error("HTTPException in create_chat")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in create_chat: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.get("/{chat_id}", response_model=ChatWithMessagesResponse)
async def get_chat(
    chat_id: int,
    limit: int = Query(20, ge=1, le=100, description="Количество сообщений для возврата (по умолчанию 20, максимум 100)."),
    chat_service: ChatService = Depends(get_chat_service),
    db: AsyncSession = Depends(get_async_session)
) -> ChatWithMessagesResponse:
    """
    Получить чат и последние N сообщений.
    """
    try:
        logger.info(f"Getting chat with id: {chat_id}")
        result = await chat_service.get_chat_with_last_messages(chat_id, limit)
        logger.info(f"Chat retrieved successfully: {chat_id}")
        return result
    except HTTPException:
        logger.error("HTTPException in get_chat")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_chat: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.delete("/{chat_id}", status_code=204)
async def delete_chat(
    chat_id: int,
    chat_service: ChatService = Depends(get_chat_service),
) -> None:
    """
    Удалить чат и все его сообщения.
    """
    try:
        logger.info(f"Deleting chat with id: {chat_id}")
        await chat_service.delete_chat(chat_id)
        logger.info(f"Chat deleted successfully: {chat_id}")
        return
    except HTTPException:
        logger.error("HTTPException in delete_chat")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in delete_chat: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred")