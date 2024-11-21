from typing import Dict, Any

from src.models.movie import Movie, MovieRatings
from src.serializers.base import BaseSerializer


class MongoMovieSerializer(BaseSerializer):
    def __init__(self):
        super().__init__(Movie)

    def serialize(self, data: Dict[str, Any]) -> Movie:
        """Преобразует данные MongoDB в Pydantic-модель."""
        data["_id"] = self.to_str(data.get("_id"))
        if "ratings" in data:
            data["ratings"] = MovieRatings(**data["ratings"])
        return self.model(**data)

    def deserialize(self, instance: Movie) -> Dict[str, Any]:
        """Преобразует Pydantic-модель в данные для MongoDB."""
        data = instance.dict(by_alias=True, exclude_none=True)
        data["_id"] = self.to_object_id(data["_id"])
        return data