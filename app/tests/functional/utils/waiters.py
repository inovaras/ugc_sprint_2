import backoff
import requests
from pymongo import MongoClient, errors as mongo_errors

from tests.functional.settings import test_settings


@backoff.on_exception(
    backoff.expo,
    Exception,
    max_tries=10,
    max_time=100,
    jitter=backoff.full_jitter,
    on_backoff=lambda details: print(f"Retrying connection to FastAPI: {details}")
)
def wait_for_app():
    """
    Ждёт доступности приложения
    """
    response = requests.get(f"http://{test_settings.service.host}:{test_settings.service.port}/api/v1/ping/health")
    assert response.status_code == 200


@backoff.on_exception(
    backoff.expo,
    mongo_errors.ConnectionFailure,
    max_tries=10,
    max_time=100,
    jitter=backoff.full_jitter,
    on_backoff=lambda details: print(f"Retrying connection to MongoDB: {details}")
)
def wait_for_mongo():
    """
    Проверяет доступность MongoDB, пытаясь установить соединение
    """
    try:
        mongo_client = MongoClient(
            host=test_settings.mongo.host,
            port=test_settings.mongo.port,
        )
        mongo_client.admin.command("ping")
    except mongo_errors.ConnectionFailure as e:
        raise mongo_errors.ConnectionFailure("MongoDB is not available") from e


def run_waiters():
    """
    Запускает последовательность ожиданий для всех необходимых сервисов.
    В данном случае ожидает доступности PostgreSQL и Redis.
    """
    wait_for_mongo()


if __name__ == '__main__':
    run_waiters()