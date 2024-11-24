from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class StorageInterface(ABC):
    @abstractmethod
    async def connect(self) -> None:
        """
        Подключение к хранилищу
        """
        pass

    @abstractmethod
    async def insert(self, collection: str, data: List[Dict]) -> None:
        """
        Вставка данных в указанное хранилище
        """
        pass

    @abstractmethod
    async def read(self, collection: str, filters: Optional[Dict[str, Any]] = None, limit: Optional[int] = None) -> List[Dict]:
        """
        Извлечение данных из указанного хранилища с фильтрацией и ограничением
        """
        pass

    @abstractmethod
    async def clear(self) -> None:
        """
        Очистка всех данных в хранилище
        """
        pass

    @abstractmethod
    async def close(self) -> None:
        """
        Закрытие соединения с хранилищем
        """
        pass