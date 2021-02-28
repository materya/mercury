# Copyright (C) 2019 - 2021 Richard Kemp
# $Id$
# -*- coding: utf-8; py-indent-offset:4 -*-

"""Common tools and classes for the library.

Provide

- metaclasses
- Generic classes
- Analyzing tools
"""


__copyright__ = "Copyright 2019 - 2021 Richard Kemp"
__revision__ = "$Id$"
__all__ = [
    "BaseClass",
    "BaseMetaClass",
    "Client",
    "DataSource",
    "DataStore",
    "FlexArray",
    "cross",
    "crossover",
    "crossunder",
]


from numbers import Number

import pandas as pd

from .baseclass import BaseClass, BaseMetaClass
from .client import Client
from .datasource import DataSource
from .datastore import DataStore
from .flexarray import FlexArray


# def argument_validator(name, *, in_tuple):
#     """Decorator helper to enforce an argument type or value

#     arguments:
#     name -- the keyword argument name to check

#     keyword arguments:
#     in_tuple -- Ensure the argument value is in this tuple
#     """
#     def decorator(function):
#         def validation(*args, **kargs):
#             value = kargs.get(name)
#             if value and in_tuple and value not in in_tuple:
#                 raise TypeError("{value} not in {tuple}"
#                                 .format(value=value, tuple=in_tuple))

#             return function(*args, **kargs)

#         return validation
#     return decorator


def crossover(series1, series2) -> bool:
    """Return `True` if `series1` just crossed over `series2`.

    >>> crossover(self.data.Close, self.sma)
    True
    """
    series1 = (series1.values if isinstance(series1, pd.Series) else
               (series1, series1) if isinstance(series1, Number) else
               series1)
    series2 = (series2.values if isinstance(series2, pd.Series) else
               (series2, series2) if isinstance(series2, Number) else
               series2)

    try:
        return series1[-2] < series2[-2] and series1[-1] > series2[-1]
    except IndexError:
        return False


def crossunder(series1, series2) -> bool:
    """Return `True` if `series1` just crossed under `series2`.

    >>> crossunder(self.data.Close, self.sma)
    True
    """
    return crossover(series2, series1)


def cross(series1, series2) -> bool:
    """Return `True` if `series1` and `series2` just crossed either direction.

    >>> cross(self.data.Close, self.sma)
    True
    """
    return crossover(series1, series2) or crossunder(series1, series2)
