from time import time

import pytest
from tort import FunctionTimeOut
from tort.implementations.threaded_timeout import (KillableThread,
                                                   threaded_timeout)

SLEEP_SEC = 2.5
X1 = 5
X2 = 13
JITTER = 0.1


def add(x, y):
    return x + y


def test_thread_success(sleepy_func_factory: callable):
    """Test Killable thread operates like a normal thread."""
    sleepy_add = sleepy_func_factory(SLEEP_SEC, add)

    kill_thread = KillableThread(target=sleepy_add, args=(X1, X2))
    kill_thread.start()
    kill_thread.join()


def test_thread_killed(infinite_loop):
    """Test Killable thread can be terminated if stuck in a loop."""
    kill_thread = KillableThread(target=infinite_loop)
    kill_thread.start()
    while kill_thread.is_alive():
        # We loop raising exception incase it's caught hopefully this breaks us far out.
        kill_thread.terminate()
        kill_thread.join(2.0)

    assert kill_thread.is_alive() is False  # nosec


def test_timeout_thread_func(infinite_loop):

    timedout_loop = threaded_timeout(infinite_loop, timeout=2.0)
    with pytest.raises(FunctionTimeOut):
        start = time()
        timedout_loop()
    stop = time()

    elapsed = stop - start
    assert (elapsed - 2.0) < JITTER  # nosec
