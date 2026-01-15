from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from typing import Optional, List

from app.models.message import Message
from .base import BaseRepository


class MessageRepository(BaseRepository[Message]):
    """
    Репозиторий для работы с сущностью Message.
    Реализует методы CRUD через SQLAlchemy.
    Также содержит дополнительные методы, специфичные для сообщений (например, получение последних N сообщений).
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, obj: Message) -> Message:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get_by_id(self, entity_id: int) -> Optional[Message]:
        query = select(Message).where(Message.id == entity_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def list(self, **filters) -> List[Message]:
        query = select(Message)
        if filters:
            for key, value in filters.items():
                if hasattr(Message, key):
                    query = query.filter(getattr(Message, key) == value)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(self, entity_id: int, **kwargs) -> Optional[Message]:
        message = await self.get_by_id(entity_id)
        if message:
            for key, value in kwargs.items():
                setattr(message, key, value)
            await self.session.commit()
            await self.session.refresh(message)
        return message

    async def delete(self, entity_id: int) -> bool:
        query = delete(Message).where(Message.id == entity_id)
        result = await self.session.execute(query)
        await self.session.commit()
        return result.rowcount > 0

    async def get_last_messages_by_chat_id(self, chat_id: int, limit: int = 20) -> List[Message]:
        """
        Получить последние N сообщений для указанного чата, отсортированных по дате создания.
        """
        query = (
            select(Message)
            .where(Message.chat_id == chat_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        result = await self.session.execute(query)
        messages = result.scalars().all()
        return messages[::-1]