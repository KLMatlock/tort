import time

import pytest


@pytest.fixture
def sleepy_func_factory() -> callable:
    """Factory function to provide an arbitrary sleep time
    to a provided callable function.

    Parameters
    ----------
    secs : float
        Number of seconds to sleep.
    function : callable
        Function to be called after sleeping

    Returns
    -------
    callable
        Same as `function` but with arbitrary delay added.
    """

    def factory(secs: float, function: callable) -> callable:
        def sleeping_function(*args, **kwargs):
            time.sleep(secs)
            return function(*args, **kwargs)

        return sleeping_function

    return factory


@pytest.fixture
def retriable_func():
    tries = 0

    def f():
        nonlocal tries
        try:
            if tries != 0:
                return True
            while True:
                time.sleep(0.1)
        finally:
            tries = 1
        return False
    return f


@pytest.fixture
def infinite_loop():
    def f():
        try:
            while True:
                time.sleep(0.1)
        # Prevents unhandled exception with pytest.
        finally:
            return

    return f
