from typing import List, Dict, Any, Optional
import asyncpg
import logging

from .base import StorageInterface

logger = logging.getLogger(__name__)


class PostgresStorage(StorageInterface):
    def __init__(self, dsn: str = "postgresql://user:password@localhost:5432/database") -> None:
        self.dsn = dsn
        self.pool = None

    async def connect(self) -> None:
        """
        Асинхронное подключение к PostgreSQL
        """
        self.pool = await asyncpg.create_pool(dsn=self.dsn)
        logger.info("Connected to PostgreSQL")
        await self._create_tables()

    async def _create_tables(self) -> None:
        """Создает необходимые таблицы в базе данных."""
        async with self.pool.acquire() as connection:
            await connection.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id UUID PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    ratings UUID[],
                    reviews UUID[],
                    bookmarks UUID[]
                );
            """)
            await connection.execute("""
                CREATE TABLE IF NOT EXISTS movies (
                    id UUID PRIMARY KEY,
                    title TEXT NOT NULL,
                    year INT NOT NULL,
                    ratings_average FLOAT,
                    ratings_count INT,
                    reviews UUID[]
                );
            """)
            await connection.execute("""
                CREATE TABLE IF NOT EXISTS ratings (
                    id UUID PRIMARY KEY,
                    user_id UUID REFERENCES users(id),
                    movie_id UUID REFERENCES movies(id),
                    rating INT,
                    timestamp TIMESTAMP
                );
            """)
            await connection.execute("""
                CREATE TABLE IF NOT EXISTS reviews (
                    id UUID PRIMARY KEY,
                    user_id UUID REFERENCES users(id),
                    movie_id UUID REFERENCES movies(id),
                    review_text TEXT,
                    likes INT,
                    dislikes INT,
                    timestamp TIMESTAMP
                );
            """)
            await connection.execute("""
                CREATE TABLE IF NOT EXISTS bookmarks (
                    id UUID PRIMARY KEY,
                    user_id UUID REFERENCES users(id),
                    movie_id UUID REFERENCES movies(id),
                    timestamp TIMESTAMP
                );
            """)
            logger.info("All necessary tables are created in PostgreSQL")

    async def _transform_data(self, data: List[Dict]) -> List[Dict]:
        """
        Преобразует данные для PostgreSQL
        """
        transformed = []
        for record in data:
            transformed_record = record.copy()
            if '_id' in transformed_record:
                transformed_record['id'] = transformed_record.pop('_id')
            transformed.append(transformed_record)
        return transformed

    async def insert(self, collection: str, data: List[Dict[str, Any]]) -> None:
        """
        Асинхронная вставка данных в указанную таблицу
        """
        if not data:
            return

        data = await self._transform_data(data)

        async with self.pool.acquire() as connection:
            async with connection.transaction():
                columns = ", ".join(data[0].keys())
                values_template = ", ".join([f"${i+1}" for i in range(len(data[0]))])
                query = f"INSERT INTO {collection} ({columns}) VALUES ({values_template})"
                for record in data:
                    await connection.execute(query, *record.values())
        logger.info(f"Inserted {len(data)} records into PostgreSQL table '{collection}'")

    async def read(self, collection: str, filters: Optional[Dict[str, Any]] = None, limit: Optional[int] = None) -> List[Dict]:
        """
        Читает данные из указанной таблицы с фильтрацией и ограничением
        """
        async with self.pool.acquire() as connection:
            query = f"SELECT * FROM {collection}"
            params = []

            if filters:
                filter_clauses = []
                for i, (column, value) in enumerate(filters.items()):
                    filter_clauses.append(f"{column} = ${i + 1}")
                    params.append(value)
                query += f" WHERE {' AND '.join(filter_clauses)}"

            if limit:
                query += f" LIMIT {limit}"

            rows = await connection.fetch(query, *params)
            return [dict(row) for row in rows]

    async def clear(self) -> None:
        """
        Удаляет все данные из всех таблиц PostgreSQL
        """
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                tables = await connection.fetch("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                """)
                for table in tables:
                    table_name = table['table_name']
                    await connection.execute(f'TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE')
        logger.info("All data cleared from PostgreSQL")

    async def close(self) -> None:
        """
        Закрывает пул соединений
        """
        if self.pool:
            await self.pool.close()
            logger.info("PostgreSQL connection pool closed")