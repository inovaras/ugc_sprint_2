from typing import Dict, Any

from src.models.user import User, UserRating
from src.serializers.base import BaseSerializer


class MongoUserSerializer(BaseSerializer):
    def __init__(self):
        super().__init__(User)

    def serialize(self, data: Dict[str, Any]) -> User:
        """Преобразует данные MongoDB в Pydantic-модель."""
        data["_id"] = self.to_str(data.get("_id"))
        if "ratings" in data:
            data["ratings"] = [UserRating(**rating) for rating in data["ratings"]]
        return self.model(**data)

    def deserialize(self, instance: User) -> Dict[str, Any]:
        """Преобразует Pydantic-модель в данные для MongoDB."""
        data = instance.dict(by_alias=True, exclude_none=True)
        data["_id"] = self.to_object_id(data["_id"])
        return data