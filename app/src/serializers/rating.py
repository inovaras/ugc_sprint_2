from typing import Dict, Any

from src.models.rating import Rating
from src.serializers.base import BaseSerializer


class MongoRatingSerializer(BaseSerializer):
    def __init__(self):
        super().__init__(Rating)

    def serialize(self, data: Dict[str, Any]) -> Rating:
        """Преобразует данные MongoDB в Pydantic-модель."""
        data["_id"] = self.to_str(data.get("_id"))  # Используем метод из базового класса
        return self.model(**data)

    def deserialize(self, instance: Rating) -> Dict[str, Any]:
        """Преобразует Pydantic-модель в данные для MongoDB."""
        data = instance.dict(by_alias=True, exclude_none=True)
        data["_id"] = self.to_object_id(data["_id"])  # Используем метод из базового класса
        return data