from abc import ABC, abstractmethod
from bson import ObjectId
from typing import TypeVar, Type, Dict, Any
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class BaseSerializer(ABC):
    model: Type[T]

    def __init__(self, model: Type[T]):
        self.model = model

    @abstractmethod
    def serialize(self, data: Dict[str, Any]) -> T:
        """Преобразует данные MongoDB в Pydantic-модель."""
        ...

    @abstractmethod
    def deserialize(self, instance: T) -> Dict[str, Any]:
        """Преобразует Pydantic-модель в данные для MongoDB."""
        ...

    @staticmethod
    def to_object_id(value: Any) -> ObjectId:
        """Преобразует строку в ObjectId, если это возможно."""
        if ObjectId.is_valid(value):
            return ObjectId(value)
        raise ValueError(f"Invalid ObjectId: {value}")

    @staticmethod
    def to_str(value: Any) -> str:
        """Преобразует ObjectId в строку."""
        return str(value) if isinstance(value, ObjectId) else value