import pytest
from typing import Callable
from fixtures import time_tracking, track_performance
import time
from datetime import timedelta

from fibonacci_app.fibonacci_logic.fibonacci_function import (
    fibonacci_recursive,
    fibonacci_custom,
    fibonacci_optimized,
)


@pytest.mark.performance
@track_performance(runtime_limit=timedelta(seconds=1))
def test_fibonaci_code_duplition() -> None:
    # To provoke a timeout, sleep for 2 seconds
    # time.sleep(2)
    assert fibonacci_custom(0) == 0
    assert fibonacci_custom(1) == 1
    assert fibonacci_custom(2) == 1
    assert fibonacci_custom(3) == 2
    assert fibonacci_custom(30) == 832040


@pytest.mark.parametrize("n, expected", [(0, 0), (1, 1), (2, 1), (30, 832040)])
def test_fibonaci_code_refactor_1(n: int, expected: int) -> None:
    assert fibonacci_custom(n) == expected


@pytest.mark.parametrize("n, expected", [(0, 0), (1, 1), (2, 1), (30, 832040)])
@pytest.mark.parametrize(
    "fib_func",
    [fibonacci_custom, fibonacci_recursive, fibonacci_optimized],
)
def test_fibonacci(
    time_tracking, fib_func: Callable[[int], int], n: int, expected: int
) -> None:
    res = fib_func(n)
    assert res == expected
