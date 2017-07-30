"""
Lazy integer arithmetic.

"""
from __future__ import print_function, division
from future.utils import with_metaclass
from builtins import range


class LazyMeta(type):
    """metaclass to simplify creation of lazy methods"""

    def __new__(meta, cls_name, bases, _dict):
        for operator in _dict.get('_operators', ()):
            _dict[operator] = LazyMethod(operator)

        return super(LazyMeta, meta).__new__(meta, cls_name, bases, _dict)


class LazyMethod(object):
    """Descriptor to easily implement arithmetic operators."""

    def __init__(self, method_name=None):
        self.method_name = method_name

    def __get__(self, instance, cls):
        def inner(*others):
            def lazy_result():
                args = [other.lazy_val() for other in others]
                method = getattr(instance.lazy_val(), self.method_name)
                return method(*args)

            return cls(lazy_result)

        return inner


class LazyBase(with_metaclass(LazyMeta, object)):
    """Inherit from this."""


class LazyInteger(LazyBase):
    """Lazy integers."""

    _operators = (
        '__add__',
        '__sub__',
        '__mul__',
        '__div__',
        '__abs__',  # works for unary operators too!
    )

    def __init__(self, lazy_val=lambda: 0):
        self.lazy_val = lazy_val

    def __call__(self):
        """Evaluation."""
        return self.lazy_val()


if __name__ == '__main__':

    a = LazyInteger(lambda: 2)
    b = LazyInteger(lambda: -3)

    assert (a + b)() == -1
    assert abs(b)() == 3
    assert (b * a)() == -6

    n = LazyInteger()

    for _ in range(500):
        n += LazyInteger(lambda: 1)

    assert n() == 500

    for _ in range(500):
        n += LazyInteger(lambda: 1)

    try:
        n()
    except RuntimeError as e:
        assert e.args[0] == 'maximum recursion depth exceeded'
    else:
        raise AssertionError('Should have caused stack overflow.')

    print('all tests pass')
