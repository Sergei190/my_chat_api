import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict # Импортируем SettingsConfigDict


class Settings(BaseSettings):
    """
    Настройки приложения, загружаемые из .env файла или переменных окружения.
    """
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "postgres")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_NAME: str = os.getenv("DB_NAME", "chat_db")

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    APP_TITLE: str = "Chat API"
    APP_VERSION: str = "1.0.0"
    API_V1_STR: str = "/v1"

    DEFAULT_MESSAGE_LIMIT: int = 20
    MAX_MESSAGE_LIMIT: int = 100
    MAX_TITLE_LENGTH: int = 200
    MAX_TEXT_LENGTH: int = 5000

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")


settings = Settings()