import pytest
from tortfunc.registry import Registry


def my_func():
    return 5


def my_func2():
    return 7


@pytest.fixture
def func_registry():
    return Registry(name="test", default_method="my_func", reg={"my_func": my_func})


def test_get_func(func_registry):
    mf = func_registry["my_func"]
    assert mf() == 5


def test_set_funct(func_registry):
    func_registry["my_func2"] = my_func2
    mf2 = func_registry["my_func2"]
    assert mf2() == 7

