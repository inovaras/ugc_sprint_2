import pytest
import logging
import json
from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
async def load_test_data(mongo_client: AsyncIOMotorClient):
    """
    Фикстура для загрузки данных из JSON в MongoDB.
    """
    logger.info("Загрузка данных в MongoDB перед тестами...")

    with open("tests/functional/data.json", "r") as file:
        test_data = json.load(file)
    
    await mongo_client.ugc.users.delete_many({})
    await mongo_client.ugc.movies.delete_many({})
    await mongo_client.ugc.ratings.delete_many({})

    await mongo_client.ugc.users.insert_many(test_data["users"])
    await mongo_client.ugc.movies.insert_many(test_data["movies"])
    await mongo_client.ugc.ratings.insert_many(test_data["ratings"])

    logger.info("Данные успешно загружены.")

    yield

    logger.info("Очистка данных после тестов...")
    await mongo_client.ugc.users.delete_many({})
    await mongo_client.ugc.movies.delete_many({})
    await mongo_client.ugc.ratings.delete_many({})
