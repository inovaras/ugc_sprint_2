from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timezone


class UserRating(BaseModel):
    movie_id: str = Field(..., description="ID фильма")
    rating: float = Field(..., ge=0, le=5, description="Оценка (от 0 до 5)")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Дата и время оценки")


class User(BaseModel):
    id: str = Field(..., alias="_id", description="Уникальный идентификатор пользователя")
    name: str = Field(..., description="Имя пользователя")
    email: EmailStr = Field(..., description="Email пользователя")
    ratings: List[UserRating] = Field(default_factory=list, description="Список оценок пользователя")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Дата регистрации")