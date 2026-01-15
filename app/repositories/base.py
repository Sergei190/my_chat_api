from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List

T = TypeVar('T')

class BaseRepository(ABC, Generic[T]):
    """
    Абстрактный базовый класс для репозиториев.
    Определяет общий интерфейс для CRUD-операций.
    """

    @abstractmethod
    async def create(self, obj: T) -> T:
        """Создать новую сущность."""
        pass

    @abstractmethod
    async def get_by_id(self, entity_id: int) -> Optional[T]:
        """Получить сущность по ID."""
        pass

    @abstractmethod
    async def list(self, **filters) -> List[T]:
        """Получить список сущностей с фильтрацией."""
        pass

    @abstractmethod
    async def update(self, entity_id: int, **kwargs) -> Optional[T]:
        """Обновить сущность по ID."""
        pass

    @abstractmethod
    async def delete(self, entity_id: int) -> bool:
        """Удалить сущность по ID."""
        pass