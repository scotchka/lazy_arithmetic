"""
Lazy integer arithmetic.

"""
from __future__ import print_function, division
from future.utils import with_metaclass
from builtins import range


class LazyMeta(type):
    def __init__(cls, *args):
        super(LazyMeta, cls).__init__(*args)
        for attr in cls.__dict__:
            if isinstance(cls.__dict__[attr], Lazy):
                cls.__dict__[attr].method_name = attr


class Lazy(object):
    """Descriptor to easily implement arithmetic operators."""

    def __get__(self, instance, cls):
        def inner(*others):
            def lazy_result():
                args = [other.lazy_val() for other in others]
                method = getattr(instance.lazy_val(), self.method_name)
                return method(*args)

            return cls(lazy_result)

        return inner


class LazyInteger(with_metaclass(LazyMeta, object)):
    """Lazy integers."""

    __metaclass__ = LazyMeta

    def __init__(self, lazy_val=lambda: 0):
        self.lazy_val = lazy_val

    __add__ = Lazy()
    __sub__ = Lazy()
    __mul__ = Lazy()
    __div__ = Lazy()
    __abs__ = Lazy()  # works for unary operators too!

    def __call__(self):
        """Evaluation."""
        return self.lazy_val()


if __name__ == '__main__':

    a = LazyInteger(lambda: 2)
    b = LazyInteger(lambda: -3)

    assert (a + b)() == -1
    assert abs(b)() == 3
    assert (b * a)() == -6

    n = LazyInteger(lambda: 0)

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
