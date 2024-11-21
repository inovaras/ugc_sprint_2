from typing import List, Optional
from pydantic import BaseModel, Field

from datetime import datetime


class MovieRatings(BaseModel):
    average: float = Field(..., ge=0, le=5, description="Средняя оценка фильма")
    count: int = Field(..., ge=0, description="Количество оценок фильма")


class Movie(BaseModel):
    id: str = Field(..., alias="_id", description="Уникальный идентификатор фильма")
    title: str = Field(..., description="Название фильма")
    year: int = Field(..., ge=1800, le=datetime.now().year, description="Год выпуска фильма")
    ratings: MovieRatings = Field(default_factory=MovieRatings, description="Рейтинги фильма")