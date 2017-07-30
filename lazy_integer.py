"""
Lazy integer arithmetic.

"""
from __future__ import print_function, division
from future.utils import with_metaclass


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

    def __init__(self, lazy_val=None):
        self.lazy_val = lazy_val or (lambda: self._type())

    def __call__(self):
        """Evaluation."""
        return self.lazy_val()


class LazyInteger(LazyBase):
    """Lazy integers.

        >>> LazyInteger()()
        0

        >>> a = LazyInteger(lambda: 2)
        >>> b = LazyInteger(lambda: -3)

        >>> (a + b)()
        -1

        >>> abs(b)()
        3

        >>> (b * a)()
        -6
    """

    _type = int

    _operators = (
        '__add__',
        '__sub__',
        '__mul__',
        '__div__',
        '__abs__',  # works for unary operators too!
    )


class LazyString(LazyBase):
    """Lazy strings.

        >>> LazyString()()
        ''

        >>> s1 = LazyString(lambda: 'hello ')
        >>> s2 = LazyString(lambda: 'world')
        >>> (s1 + s2)()
        'hello world'
    """

    _type = str

    _operators = (
        '__add__',
    )
