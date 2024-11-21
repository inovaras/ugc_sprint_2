from motor.motor_asyncio import AsyncIOMotorClient
from typing import AsyncGenerator, List, Dict

class MongoDBClient:
    def __init__(self, mongo_url: str):
        self.client = AsyncIOMotorClient(mongo_url)
        self.db = self.client["ugc"]

    async def insert_many(self, collection_name: str, data: List[Dict]):
        await self.db[collection_name].insert_many(data)

    async def close(self):
        self.client.close()