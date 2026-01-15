from typing import Optional, List
from app.repositories.chat_repository import ChatRepository
from app.repositories.message_repository import MessageRepository
from app.models.chat import Chat
from app.models.message import Message
from fastapi import HTTPException


class ChatService:
    """
    Сервис для бизнес-логики, связанной с чатами.
    """

    def __init__(self, chat_repo: ChatRepository, message_repo: MessageRepository):
        self.chat_repo = chat_repo
        self.message_repo = message_repo

    async def create_chat(self, title: str) -> Chat:
        """
        Создать новый чат.
        """
        title = title.strip()
        if not title or len(title) > 200:
            raise HTTPException(status_code=422, detail="Title must be 1-200 characters long.")

        new_chat = Chat(title=title)
        return await self.chat_repo.create(new_chat)

    async def get_chat_with_last_messages(self, chat_id: int, limit: int = 20) -> dict:
        """
        Получить чат и последние N сообщений.
        """
        chat = await self.chat_repo.get_by_id(chat_id)
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")

        messages = await self.message_repo.get_last_messages_by_chat_id(chat_id, limit)
        return {
            "chat": chat,
            "messages": messages
        }

    async def delete_chat(self, chat_id: int) -> bool:
        """
        Удалить чат. Сообщения удаляются каскадно через ORM.
        """
        success = await self.chat_repo.delete(chat_id)
        if not success:
            raise HTTPException(status_code=404, detail="Chat not found")
        return True