import pytest

from motor.motor_asyncio import AsyncIOMotorClient

from tests.functional.settings import test_settings


@pytest.fixture(scope="session")
async def mongo_client():
    """
    Подключение к MongoDB для тестов
    """
    client = AsyncIOMotorClient(test_settings.mongo.url)
    yield client
    client.close()