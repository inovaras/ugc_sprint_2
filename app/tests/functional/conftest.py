import asyncio
import pytest


pytest_plugins = [
    'tests.functional.fixtures.http',
    'tests.functional.fixtures.mongo',
    'tests.functional.fixtures.data',
]


@pytest.fixture(scope='session', autouse=True)
def event_loop():
    """
    Создает и предоставляет asyncio event loop для всех тестов в сессии
    """

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop

    loop.close()