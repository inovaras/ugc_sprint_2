import argparse
import asyncio

from src.db import MongoDBClient
from src.generators import generate_users, generate_movies, generate_ratings


async def clear_collections(mongo_client: MongoDBClient, collections: list[str]):
    """
    Очищает указанные коллекции.
    """
    for collection in collections:
        print(f"Очистка коллекции {collection}...")
        await mongo_client.db[collection].delete_many({})
    print("Очистка завершена!")


async def main(args):
    mongo_client = MongoDBClient(args.mongo_url)

    # Очистка коллекций
    if args.clear:
        await clear_collections(mongo_client, [args.user_collection, args.movie_collection, args.rating_collection])
        return  # Завершаем выполнение, если требуется только очистка

    # Генерация пользователей
    users = []
    print(f"Генерация {args.count_users} пользователей...")
    async for batch in generate_users(count=args.count_users, batch_size=args.batch_size):
        if not args.dry_run:
            await mongo_client.insert_many(args.user_collection, batch)
        users.extend(batch)

    # Генерация фильмов
    movies = []
    print(f"Генерация {args.count_movies} фильмов...")
    async for batch in generate_movies(count=args.count_movies, batch_size=args.batch_size):
        if not args.dry_run:
            await mongo_client.insert_many(args.movie_collection, batch)
        movies.extend(batch)

    # Генерация рейтингов
    print(f"Генерация {args.count_ratings} рейтингов...")
    async for batch in generate_ratings(
        count=args.count_ratings,
        batch_size=args.batch_size,
        users=users,
        movies=movies,
    ):
        if not args.dry_run:
            await mongo_client.insert_many(args.rating_collection, batch)

    # Обновление пользователей и фильмов с учётом рейтингов
    if not args.dry_run:
        print("Обновление пользователей и фильмов...")
        await mongo_client.db[args.user_collection].delete_many({})
        await mongo_client.db[args.user_collection].insert_many(users)
        await mongo_client.db[args.movie_collection].delete_many({})
        await mongo_client.db[args.movie_collection].insert_many(movies)

    await mongo_client.close()
    print("Генерация завершена!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Генератор данных для MongoDB.")

    # Параметры MongoDB
    parser.add_argument("--mongo-url", type=str, default="mongodb://localhost:27019", help="URL для подключения к MongoDB.")
    parser.add_argument("--db-name", type=str, default="ugc", help="Название базы данных.")
    parser.add_argument("--user-collection", type=str, default="users", help="Название коллекции для пользователей.")
    parser.add_argument("--movie-collection", type=str, default="movies", help="Название коллекции для фильмов.")
    parser.add_argument("--rating-collection", type=str, default="ratings", help="Название коллекции для рейтингов.")

    # Параметры генерации
    parser.add_argument("--count-users", type=int, default=1000, help="Количество пользователей для генерации.")
    parser.add_argument("--count-movies", type=int, default=500, help="Количество фильмов для генерации.")
    parser.add_argument("--count-ratings", type=int, default=10000, help="Количество рейтингов для генерации.")
    parser.add_argument("--batch-size", type=int, default=100, help="Размер одной пачки данных для вставки.")

    # Логические параметры
    parser.add_argument("--dry-run", action="store_true", help="Не вставлять данные в базу, только генерировать.")
    parser.add_argument("--clear", action="store_true", help="Очистить все коллекции перед генерацией данных.")

    args = parser.parse_args()
    asyncio.run(main(args))
