import pytest
from lazy_integer import LazyInteger


def test_no_overflow():
    n = LazyInteger()

    for _ in range(500):
        n += LazyInteger(lambda: 1)

    assert n() == 500


def test_overflow():
    n = LazyInteger()

    for _ in range(1000):
        n += LazyInteger(lambda: 1)

    with pytest.raises(RuntimeError):
        n()  # should overflow call stack
