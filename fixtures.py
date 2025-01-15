import pytest
from datetime import datetime, timedelta
from typing import Callable


@pytest.fixture
def time_tracking():
    now = datetime.now()
    yield
    elapsed = datetime.now() - now
    print(f"\nElapsed time: {elapsed.total_seconds()} seconds")


class PerformanceException(Exception):
    def __init__(self, runtime: timedelta, limit: timedelta):
        self.runtime = runtime
        self.limit = limit

    def __str__(self) -> str:
        return f"Performance test failed: (elapsed {self.runtime.total_seconds()} secs., limit {self.limit.total_seconds()} secs.)"


def track_performance(runtime_limit=timedelta(seconds=2)):
    def decorator(method: Callable):
        def wrapper(*args, **kwargs):
            start_time = datetime.now()
            result = method(
                *args, **kwargs
            )  # Pasamos todos los argumentos a la función original
            elapsed = datetime.now() - start_time

            if elapsed > runtime_limit:
                raise PerformanceException(runtime=elapsed, limit=runtime_limit)
            return result

        return wrapper

    return decorator
