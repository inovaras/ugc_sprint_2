from http import HTTPStatus
from typing import List

from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.models.rating import Rating
from src.models.base import BasePaginationParams
from src.serializers.base import BaseSerializer
from src.repositories.rating import BaseRatingRepository


class RatingService:

    def __init__(self, repository: BaseRatingRepository, serializer: BaseSerializer):
        self.repo = repository
        self.serializer = serializer

    async def get_ratings(self, params: BasePaginationParams, movie_id: str) -> List[Rating]:
        """
        Возвращает список лайков по ID фильма.
        """
        scores = await self.repo.get_ratings(params, movie_id)

        if not scores:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"No ratings found for movie with ID {movie_id}"
            )

        return scores