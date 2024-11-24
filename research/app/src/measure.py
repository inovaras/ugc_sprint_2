import logging
import time
from typing import Callable, Any

logger = logging.getLogger(__name__)


def measure_time(func: Callable) -> Callable:
    """
    Декоратор для замера времени выполнения функции.
    """
    async def wrapper(*args: Any, **kwargs: Any):
        start_time = time.time()
        result = await func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        return result, elapsed_time
    return wrapper