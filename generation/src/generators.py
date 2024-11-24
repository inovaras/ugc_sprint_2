import asyncio

from faker import Faker
from typing import List, Dict, AsyncGenerator
from uuid import uuid4
from random import randint, uniform

fake = Faker()


async def generate_users(count: int, batch_size: int) -> AsyncGenerator[List[Dict], None]:
    """
    Асинхронно генерирует пользователей
    """
    batch = []
    for _ in range(count):
        batch.append({
            "_id": str(uuid4()),
            "name": fake.name(),
            "email": fake.email(),
            "ratings": []  # Позже заполним ID оценок
        })
        if len(batch) == batch_size:
            yield batch
            batch = []
            await asyncio.sleep(0)
    if batch:
        yield batch

async def generate_movies(count: int, batch_size: int) -> AsyncGenerator[List[Dict], None]:
    """
    Асинхронно генерирует фильмы
    """
    batch = []
    for _ in range(count):
        batch.append({
            "_id": str(uuid4()),
            "title": fake.sentence(nb_words=3),
            "release_year": randint(1950, 2024),
            "ratings": {
                "average": 0,
                "count": 0
            }
        })
        if len(batch) == batch_size:
            yield batch
            batch = []
            await asyncio.sleep(0)
    if batch:
        yield batch

async def generate_ratings(count: int, batch_size: int, users: List[Dict], movies: List[Dict]) -> AsyncGenerator[List[Dict], None]:
    """
    Асинхронно генерирует рейтинги и обновляет данные пользователей и фильмов
    """
    batch = []
    for _ in range(count):
        user = fake.random_element(users)
        movie = fake.random_element(movies)
        rating_value = round(uniform(1.0, 5.0), 1)

        rating = {
            "_id": str(uuid4()),
            "user_id": user["_id"],
            "movie_id": movie["_id"],
            "rating": rating_value,
            "timestamp": fake.date_time_this_year().isoformat()
        }

        user["ratings"].append(rating["_id"])
        movie["ratings"]["average"] = (
            (movie["ratings"]["average"] * movie["ratings"]["count"] + rating_value) / (movie["ratings"]["count"] + 1)
        )
        movie["ratings"]["count"] += 1

        batch.append(rating)
        if len(batch) == batch_size:
            yield batch
            batch = []
            await asyncio.sleep(0)
    if batch:
        yield batch
