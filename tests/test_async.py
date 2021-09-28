import asyncio

import pytest
from tortfunc import FunctionTimeOut
from tortfunc.timeout.async_timeout import asyncio_timeout

SLEEP_SEC = 2.5


def sleeping_func(sleep_time: int, sleep_delta=0.1):
    async def f():
        current_time = sleep_time
        completed = False
        try:
            while current_time > 0:
                await asyncio.sleep(sleep_delta)
                current_time = current_time - sleep_delta
            completed = True
        finally:
            return completed

    return f


def test_thread_success(sleepy_func_factory: callable):
    """Test Killable thread operates like a normal thread."""
    sleep_fun = sleeping_func(SLEEP_SEC)

    async_timeout = asyncio_timeout(sleep_fun, timeout=2 * SLEEP_SEC)

    async def main():
        res = await async_timeout()
        assert res  # nosec

    asyncio.run(main())


def test_thread_killed(infinite_loop):
    """Test Killable thread can be terminated if stuck in a loop."""
    sleep_fun = sleeping_func(SLEEP_SEC)

    async_timeout = asyncio_timeout(sleep_fun, timeout=0.5 * SLEEP_SEC)

    async def main():
        await async_timeout()

    with pytest.raises(FunctionTimeOut):
        asyncio.run(main())
