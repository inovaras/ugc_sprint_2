from uuid import UUID
from typing import Annotated

from fastapi import APIRouter, status, Path, Depends


from src.models.rating import Rating
from src.models.movie import Movie
from src.models.base import BasePaginationParams

from src.dependencies.base import get_pagination_params
from src.dependencies.rating import get_rating_service
from src.services.rating import RatingService

router = APIRouter()


@router.get(path="/movie/{movie_id}/",
    status_code=status.HTTP_200_OK,
    description="Получить все оценки по ID фильма",
)
async def get_ratings(
    pagination: Annotated[BasePaginationParams, Depends(get_pagination_params)],
    rating_service: Annotated[RatingService, Depends(get_rating_service)],
    movie_id: UUID = Path(..., description='UUID фильма'),
) -> list[Rating]:
    return await rating_service.get_ratings(pagination, movie_id)