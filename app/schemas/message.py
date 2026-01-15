from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class MessageBase(BaseModel):
    """
    Базовая схема для сообщения.
    """
    text: str = Field(..., min_length=1, max_length=5000, description="Текст сообщения, длина 1-5000 символов.")


class MessageCreate(MessageBase):
    """
    Схема для создания нового сообщения.
    """
    pass


class MessageResponse(MessageBase):
    """
    Схема для ответа API с информацией о сообщении.
    """
    id: int
    chat_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)