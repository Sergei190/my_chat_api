from typing import List
from app.repositories.chat_repository import ChatRepository
from app.repositories.message_repository import MessageRepository
from app.models.message import Message
from fastapi import HTTPException


class MessageService:
    """
    Сервис для бизнес-логики, связанной с сообщениями.
    """

    def __init__(self, chat_repo: ChatRepository, message_repo: MessageRepository):
        self.chat_repo = chat_repo
        self.message_repo = message_repo

    async def send_message(self, chat_id: int, text: str) -> Message:
        """
        Отправить сообщение в чат.
        """
        chat = await self.chat_repo.get_by_id(chat_id)
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")

        text = text.strip()
        if not text or len(text) > 5000:
            raise HTTPException(status_code=422, detail="Text must be 1-5000 characters long.")

        new_message = Message(chat_id=chat_id, text=text)
        return await self.message_repo.create(new_message)

    async def get_messages_for_chat(self, chat_id: int, limit: int = 20) -> List[Message]:
        """
        Получить последние N сообщений для чата.
        """
        chat = await self.chat_repo.get_by_id(chat_id)
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")

        messages = await self.message_repo.get_last_messages_by_chat_id(chat_id, limit)
        return messages