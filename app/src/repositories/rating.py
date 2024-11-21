from abc import ABC, abstractmethod
from typing import Any
from http import HTTPStatus

from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.models.base import BasePaginationParams
from src.models.rating import Rating

class BaseRatingRepository(ABC):

    @abstractmethod
    async def get_ratings(self) -> list[dict[str, Any]]:
        ...


class MongoRatingRepository(BaseRatingRepository):

    def __init__(self, mongo: AsyncIOMotorDatabase):
        self.mongo_db = mongo
        self.collection_name = "ratings"

    async def get_ratings(self, params: BasePaginationParams, movie_id: str) -> list[Rating]:
        """
        Достаёт лайки из MongoDB по ID фильма с пагинацией
        """
        try:
            # Параметры пагинации
            skip = params.offset
            limit = params.limit

            # Запрос в MongoDB
            likes_cursor = self.mongo_db[self.collection_name].find(
                {"movie_id": str(movie_id)}
            ).skip(skip).limit(limit)

            likes = [Rating(**like) async for like in likes_cursor]

            return likes

        except Exception as exc:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Error while getting likes: {str(exc)}",
            )