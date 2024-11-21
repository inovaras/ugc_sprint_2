from functools import lru_cache
from motor.motor_asyncio import AsyncIOMotorClient

from fastapi import Depends

from src.db.mongo import get_mongo_db
from src.services.rating import RatingService
from src.repositories.rating import MongoRatingRepository
from src.serializers.rating import MongoRatingSerializer


@lru_cache()
def get_rating_service(
        mongo: AsyncIOMotorClient = Depends(get_mongo_db),
) -> RatingService:
    repository = MongoRatingRepository(mongo)
    serializer = MongoRatingSerializer()
    return RatingService(repository=repository, serializer=serializer)