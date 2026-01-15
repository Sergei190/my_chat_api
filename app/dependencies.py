from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.repositories.chat_repository import ChatRepository
from app.repositories.message_repository import MessageRepository
from app.services.chat_service import ChatService
from app.services.message_service import MessageService
import logging

logger = logging.getLogger(__name__)

async def get_chat_repository(db_session: AsyncSession = Depends(get_async_session)) -> ChatRepository:
    logger.info("Creating ChatRepository instance")
    return ChatRepository(session=db_session)


async def get_message_repository(db_session: AsyncSession = Depends(get_async_session)) -> MessageRepository:
    logger.info("Creating MessageRepository instance")
    return MessageRepository(session=db_session)


async def get_chat_service(
    chat_repo: ChatRepository = Depends(get_chat_repository),
    message_repo: MessageRepository = Depends(get_message_repository),
) -> ChatService:
    logger.info("Creating ChatService instance")
    return ChatService(chat_repo=chat_repo, message_repo=message_repo)


async def get_message_service(
    chat_repo: ChatRepository = Depends(get_chat_repository),
    message_repo: MessageRepository = Depends(get_message_repository),
) -> MessageService:
    logger.info("Creating MessageService instance")
    return MessageService(chat_repo=chat_repo, message_repo=message_repo)