from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from typing import Optional, List

from app.models.chat import Chat
from .base import BaseRepository


class ChatRepository(BaseRepository[Chat]):
    """
    Репозиторий для работы с сущностью Chat.
    Реализует методы CRUD через SQLAlchemy.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, obj: Chat) -> Chat:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get_by_id(self, entity_id: int) -> Optional[Chat]:
        query = select(Chat).where(Chat.id == entity_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def list(self, **filters) -> List[Chat]:
        query = select(Chat)
        if filters:
            for key, value in filters.items():
                if hasattr(Chat, key):
                    query = query.filter(getattr(Chat, key) == value)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(self, entity_id: int, **kwargs) -> Optional[Chat]:
        chat = await self.get_by_id(entity_id)
        if chat:
            for key, value in kwargs.items():
                setattr(chat, key, value)
            await self.session.commit()
            await self.session.refresh(chat)
        return chat

    async def delete(self, entity_id: int) -> bool:
        query = delete(Chat).where(Chat.id == entity_id)
        result = await self.session.execute(query)
        await self.session.commit()
        return result.rowcount > 0