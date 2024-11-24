import argparse
import asyncio
import logging
from typing import Dict, Any

from src.storages.base import StorageInterface
from src.storages.mongo import MongoStorage
from src.storages.postgres import PostgresStorage
from src.config import settings
from src.generators import generate_users, generate_movies, generate_ratings, generate_reviews, generate_bookmarks
from src.measure import measure_time
from src.results import save_results_to_file


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

@measure_time
async def insert_data(storage: StorageInterface, args) -> None:
    logger.info(f"Генерация {args.count_users} пользователей...")
    users = []
    async for batch in generate_users(count=args.count_users, batch_size=args.batch_size):
        await storage.insert('users', batch)
        users.extend(batch)

    logger.info(f"Генерация {args.count_movies} фильмов...")
    movies = []
    async for batch in generate_movies(count=args.count_movies, batch_size=args.batch_size):
        await storage.insert('movies', batch)
        movies.extend(batch)

    logger.info(f"Генерация {args.count_ratings} рейтингов...")
    async for batch in generate_ratings(
        count=args.count_ratings,
        batch_size=args.batch_size,
        users=users,
        movies=movies,
    ):
        await storage.insert('ratings', batch)

    logger.info(f"Генерация {args.count_reviews} рецензий...")
    async for batch in generate_reviews(
        count=args.count_reviews,
        batch_size=args.batch_size,
        users=users,
        movies=movies,
    ):
        await storage.insert('reviews', batch)

    logger.info(f"Генерация {args.count_bookmarks} закладок...")
    async for batch in generate_bookmarks(
        count=args.count_bookmarks,
        batch_size=args.batch_size,
        users=users,
        movies=movies,
    ):
        await storage.insert('bookmarks', batch)


@measure_time
async def read_data(storage: StorageInterface) -> Dict[str, Dict[str, Any]]:
    """
    Читает данные из всех таблиц/коллекций и возвращает время выполнения и количество записей для каждой
    """
    results = {}

    users, elapsed_time_users = await measure_time(storage.read)('users')
    results["users"] = {"count": len(users), "time": elapsed_time_users}
    logger.info(f"Прочитано {len(users)} записей из таблицы 'users' за {elapsed_time_users:.6f} секунд.")

    movies, elapsed_time_movies = await measure_time(storage.read)('movies')
    results["movies"] = {"count": len(movies), "time": elapsed_time_movies}
    logger.info(f"Прочитано {len(movies)} записей из таблицы 'movies' за {elapsed_time_movies:.6f} секунд.")

    ratings, elapsed_time_ratings = await measure_time(storage.read)('ratings')
    results["ratings"] = {"count": len(ratings), "time": elapsed_time_ratings}
    logger.info(f"Прочитано {len(ratings)} записей из таблицы 'ratings' за {elapsed_time_ratings:.6f} секунд.")

    reviews, elapsed_time_reviews = await measure_time(storage.read)('reviews')
    results["reviews"] = {"count": len(reviews), "time": elapsed_time_reviews}
    logger.info(f"Прочитано {len(reviews)} записей из таблицы 'reviews' за {elapsed_time_reviews:.6f} секунд.")

    bookmarks, elapsed_time_bookmarks = await measure_time(storage.read)('bookmarks')
    results["bookmarks"] = {"count": len(bookmarks), "time": elapsed_time_bookmarks}
    logger.info(f"Прочитано {len(bookmarks)} записей из таблицы 'bookmarks' за {elapsed_time_bookmarks:.6f} секунд.")

    return results


async def main() -> None:
    parser = argparse.ArgumentParser(description="Storage Research Tool")
    parser.add_argument("--storage", choices=["mongodb", "postgres"], required=True, help="Specify the storage type to test")
    parser.add_argument("--count-users", type=int, default=100, help="Number of users to generate")
    parser.add_argument("--count-movies", type=int, default=100, help="Number of movies to generate")
    parser.add_argument("--count-ratings", type=int, default=500, help="Number of ratings to generate")
    parser.add_argument("--count-reviews", type=int, default=300, help="Number of reviews to generate")
    parser.add_argument("--count-bookmarks", type=int, default=200, help="Number of bookmarks to generate")
    parser.add_argument("--batch-size", type=int, default=50, help="Batch size for data insertion")
    parser.add_argument("--clear", action="store_true", help="Clear all data from the database before generating new data")
    args = parser.parse_args()

    if args.storage == "mongodb":
        storage = MongoStorage(url=settings.mongo.url, db_name=settings.mongo.db)
    elif args.storage == "postgres":
        storage = PostgresStorage(dsn=settings.postgres.dsn)

    await storage.connect()

    if args.clear:
        logger.info("Clearing all data...")
        await storage.clear()

    results = {"storage": args.storage, "insert": {}, "read": {}}

    logger.info("Генерация и вставка данных в хранилище...")
    _, elapsed_insert_time = await insert_data(storage, args)
    results["insert"] = {
        "batch_size": args.batch_size,
        "total_records": sum([args.count_users, args.count_movies, args.count_ratings]),
        "total_time": elapsed_insert_time,
        "avg_time_per_record": elapsed_insert_time / sum([args.count_users, args.count_movies, args.count_ratings])
    }

    logger.info("Чтение всех данных из хранилища...")
    results["read"] = await read_data(storage)

    await storage.close()

    save_results_to_file(results)


if __name__ == "__main__":
    asyncio.run(main())