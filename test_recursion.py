import pytest
from lazy import LazyInteger


def test_no_overflow():
    n = LazyInteger.lazify(0)

    for _ in range(500):
        n += LazyInteger(lambda: 1)

    assert n.value == 500


def test_overflow():
    n = LazyInteger.lazify(0)

    for _ in range(1000):
        n += LazyInteger(lambda: 1)

    with pytest.raises(RuntimeError):
        n.value  # should overflow call stack
