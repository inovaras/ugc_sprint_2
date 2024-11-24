import logging
from typing import List, Dict, Any, Optional
from motor.motor_asyncio import AsyncIOMotorClient

from .base import StorageInterface

logger = logging.getLogger(__name__)

class MongoStorage(StorageInterface):
    def __init__(self,
                 url: str = 'mongodb://localhost:27017',
                 db_name: str = 'database'):
        self.uri = url
        self.db_name = db_name
        self.client = None
        self.db = None

    async def connect(self) -> None:
        """
        Асинхронное подключение к MongoDB
        """
        self.client = AsyncIOMotorClient(self.uri)
        self.db = self.client[self.db_name]
        logger.info(f"Connected to MongoDB at {self.uri}")

    async def insert(self, collection: str, data: List[Dict]):
        """
        Асинхронная вставка данных в коллекцию MongoDB
        """
        if not data:
            return

        await self.db[collection].insert_many(data)
        logger.info(f"Inserted {len(data)} records into MongoDB collection '{collection}'")

    async def read(self, collection: str, filters: Optional[Dict[str, Any]] = None, limit: Optional[int] = None) -> List[Dict]:
        """
        Читает данные из указанной коллекции с фильтрацией и ограничением
        """
        filters = filters or {}
        cursor = self.db[collection].find(filters)

        if limit:
            cursor = cursor.limit(limit)

        documents = await cursor.to_list()
        logger.info(f"Read {len(documents)} documents from collection '{collection}'")
        return documents

    async def clear(self) -> None:
        """
        Удаляет все данные из всех коллекций MongoDB
        """
        collections = await self.db.list_collection_names()
        for collection in collections:
            await self.db[collection].delete_many({})
        logger.info("All data cleared from MongoDB")

    async def close(self):
        """
        Закрывает соединение с MongoDB
        """
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")