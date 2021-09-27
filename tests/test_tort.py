import pytest
from tortfunc import FunctionTimeOut
from tortfunc.retry import timeout_retry

timeout_manifest = {"method": "thread", "spec": {"timeout": 2.5}}


def test_fulltimeout(infinite_loop):

    fail_func = timeout_retry(timeout_manifest=timeout_manifest, max_time=5)
    wrapped_func = fail_func(infinite_loop)
    with pytest.raises(FunctionTimeOut):
        wrapped_func()


def test_retry(retriable_func):

    fail_func = timeout_retry(timeout_manifest=timeout_manifest, max_time=5)
    wrapped_func = fail_func(retriable_func)
    result = wrapped_func()
    assert result  # nosec
