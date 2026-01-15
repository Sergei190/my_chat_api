import re
from typing import Optional


def validate_and_trim_title(title: str) -> str:
    """
    Триммит строку и проверяет, что она не пустая и не превышает 200 символов.
    """
    title = title.strip()
    if not title:
        raise ValueError("Title cannot be empty after trimming.")
    if len(title) > 200:
        raise ValueError("Title must be no more than 200 characters long.")
    return title


def validate_and_trim_text(text: str) -> str:
    """
    Триммит строку и проверяет, что она не пустая и не превышает 5000 символов.
    """
    text = text.strip()
    if not text:
        raise ValueError("Text cannot be empty after trimming.")
    if len(text) > 5000:
        raise ValueError("Text must be no more than 5000 characters long.")
    return text


def is_valid_chat_id(chat_id: int) -> bool:
    """
    Проверяет, что ID чата — положительное целое число.
    """
    return isinstance(chat_id, int) and chat_id > 0


def is_valid_limit(limit: int) -> int:
    """
    Проверяет и нормализует значение limit (1 <= limit <= 100).
    Возвращает нормализованное значение.
    """
    if not isinstance(limit, int):
        raise ValueError("Limit must be an integer.")
    if limit < 1:
        raise ValueError("Limit must be at least 1.")
    if limit > 100:
        raise ValueError("Limit must be no more than 100.")
    return limit