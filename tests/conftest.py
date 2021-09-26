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
def infinite_loop():
    def f():
        while True:
            time.sleep(0.1)
    return f
