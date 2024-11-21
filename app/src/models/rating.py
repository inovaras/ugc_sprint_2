from pydantic import BaseModel, Field
from datetime import datetime, timezone


class Rating(BaseModel):
    id: str = Field(..., alias="_id", description="Уникальный идентификатор оценки")
    user_id: str = Field(..., description="ID пользователя, который поставил оценку")
    movie_id: str = Field(..., description="ID фильма, которому поставлена оценка")
    rating: float = Field(..., ge=0, le=5, description="Оценка (от 0 до 5)")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Дата и время оценки")