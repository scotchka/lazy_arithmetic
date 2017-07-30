"""
Lazy integer arithmetic.

"""
from __future__ import print_function, division
from future.utils import with_metaclass


class LazyMeta(type):
    """Metaclass to simplify creation of lazy methods."""

    def __new__(meta, cls_name, bases, _dict):
        for operator in _dict.get('_operators', ()):
            _dict[operator] = LazyMethod(operator)

        _dict.pop('_operators', None)

        return super(LazyMeta, meta).__new__(meta, cls_name, bases, _dict)

    def lazify(cls, value):
        """Helper function to wrap literal values.

            >>> (LazyInteger.lazify(2) + LazyInteger.lazify(3))()
            5

            >>> LazyInteger.lazify(-100)() == LazyInteger(lambda: -100)()
            True

            >>> isinstance(LazyString.lazify('hello'), LazyString)
            True
        """
        return cls(lambda: value)


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

    @property
    def value(self):
        """Evaluates and returns value.

            >>> LazyInteger.lazify(-9).value
            -9
        """
        return self.__call__()


class LazyInteger(LazyBase):
    """Lazy integers.

        >>> LazyInteger().value
        0

        >>> a = LazyInteger.lazify(2)
        >>> b = LazyInteger.lazify(-3)

        >>> (a + b).value
        -1

        >>> abs(b).value
        3

        >>> (b * a).value
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

        >>> s1 = LazyString.lazify('hello ')
        >>> s2 = LazyString.lazify('world')
        >>> (s1 + s2).value
        'hello world'
    """

    _type = str

    _operators = (
        '__add__',
    )
