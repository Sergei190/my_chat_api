from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List, Optional
from .message import MessageResponse


class ChatBase(BaseModel):
    """
    Базовая схема для чата.
    """
    title: str = Field(..., min_length=1, max_length=200, description="Заголовок чата, длина 1-200 символов.")


class ChatCreate(ChatBase):
    """
    Схема для создания нового чата.
    """
    pass


class ChatResponse(ChatBase):
    """
    Схема для ответа API с информацией о чате.
    """
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChatWithMessagesResponse(BaseModel):
    """
    Схема для ответа API с информацией о чате и его последними сообщениями.
    """
    chat: ChatResponse
    messages: List[MessageResponse]

    model_config = ConfigDict(from_attributes=True)