from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models.chat import Chat
from app.repositories.chat_repository import ChatRepository


async def get_chat_or_404(
    chat_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> Chat:
    """
    Вспомогательная зависимость: получает чат по ID или выбрасывает 404.
    Может использоваться в роутах, где нужно гарантировать существование чата.
    """
    repo = ChatRepository(session)
    chat = await repo.get_by_id(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat