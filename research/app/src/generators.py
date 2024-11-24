import asyncio
from faker import Faker
from typing import List, Dict, AsyncGenerator
from uuid import uuid4
from random import randint, uniform, choice

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
            "ratings": [],
            "reviews": [],
            "bookmarks": []
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
            "year": randint(1950, 2024),
            "ratings_average": 0,
            "ratings_count": 0,
            "reviews": []
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
            "timestamp": fake.date_time_this_year()
        }

        user["ratings"].append(rating["_id"])
        movie["ratings_average"] = (
            (movie["ratings_average"] * movie["ratings_count"] + rating_value) / (movie["ratings_count"] + 1)
        )
        movie["ratings_count"] += 1

        batch.append(rating)
        if len(batch) == batch_size:
            yield batch
            batch = []
            await asyncio.sleep(0)
    if batch:
        yield batch

async def generate_reviews(count: int, batch_size: int, users: List[Dict], movies: List[Dict]) -> AsyncGenerator[List[Dict], None]:
    """
    Асинхронно генерирует рецензии и обновляет данные пользователей и фильмов
    """
    batch = []
    for _ in range(count):
        user = fake.random_element(users)
        movie = fake.random_element(movies)

        review = {
            "_id": str(uuid4()),
            "user_id": user["_id"],
            "movie_id": movie["_id"],
            "review_text": fake.text(max_nb_chars=200),
            "likes": randint(0, 100),
            "dislikes": randint(0, 50),
            "timestamp": fake.date_time_this_year()
        }

        user["reviews"].append(review["_id"])
        movie["reviews"].append(review["_id"])

        batch.append(review)
        if len(batch) == batch_size:
            yield batch
            batch = []
            await asyncio.sleep(0)
    if batch:
        yield batch

async def generate_bookmarks(count: int, batch_size: int, users: List[Dict], movies: List[Dict]) -> AsyncGenerator[List[Dict], None]:
    """
    Асинхронно генерирует закладки и обновляет данные пользователей
    """
    batch = []
    for _ in range(count):
        user = fake.random_element(users)
        movie = fake.random_element(movies)

        bookmark = {
            "_id": str(uuid4()),
            "user_id": user["_id"],
            "movie_id": movie["_id"],
            "timestamp": fake.date_time_this_year()
        }

        user["bookmarks"].append(bookmark["_id"])

        batch.append(bookmark)
        if len(batch) == batch_size:
            yield batch
            batch = []
            await asyncio.sleep(0)
    if batch:
        yield batch
