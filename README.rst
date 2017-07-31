.. image:: https://travis-ci.org/scotchka/lazy_arithmetic.svg?branch=master
  :target: https://travis-ci.org/scotchka/lazy_arithmetic
.. image:: https://coveralls.io/repos/github/scotchka/lazy_arithmetic/badge.svg?branch=master
  :target: https://coveralls.io/github/scotchka/lazy_arithmetic?branch=master

Lazy Arithmetic
---------------

Implement lazy evaluation in Python.

.. code::

  from lazy import LazyBase

  class LazyInteger(LazyBase):
    _type = int

    _operators = ('__add__',)
