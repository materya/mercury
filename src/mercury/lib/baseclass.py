# Copyright (C) 2019 - 2021 Richard Kemp
# $Id$
# -*- coding: utf-8; py-indent-offset:4 -*-

"""Mercury Base Class module.

Provides:
    - BaseClass default class inheritance
    - BaseMetaClass default metaclass for interface classes
"""

__copyright__ = "Copyright 2019 - 2021 Richard Kemp"
__revision__ = "$Id$"
__all__ = [
    "BaseClass",
    "BaseMetaClass",
]


import logging
from abc import ABCMeta


class MetaBase(type):
    """BaseClass metaclass.

    Generate a `__logger` method for any subclass, standardizing the way
    to log information accross the whole library.
    """
    def __init__(cls, *args) -> None:
        """Initialize class."""
        super().__init__(*args)

        # Explicit name mangling
        logger_attribute_name = "_" + cls.__name__ + "__logger"

        # Logger name derived accounting for inheritance for the bonus marks
        # logger_name = ".".join([c.__name__ for c in cls.__mro__[-2::-1]])
        package_name = cls.__module__.split(".")[0]
        logger_name = ".".join([package_name, cls.__name__])

        setattr(cls, logger_attribute_name, logging.getLogger(logger_name))


class BaseClass(metaclass=MetaBase):
    """Mercury BaseClass.

    This class is used as the main inheritance for all Mercury classes
    and provides default methods and properties across all the library.
    """
    def __repr__(self) -> str:
        """Improved default __repr__ value."""
        def quote(item: tuple) -> tuple:
            """Add quotes to a string value in a tuple."""
            (key, value) = item
            value = f"'{value}'" if isinstance(value, str) else value
            return (key, value)

        values = ",".join("{}={}".format(*item) for item in
                          map(quote, vars(self).items()))
        return f"{type(self).__name__}({values})"


class BaseMetaClass(ABCMeta, type(BaseClass)):
    """Base metaclass for Interface classes.

    This trick is needed when you want to use more than one metaclass
    for a given class.
    """
    pass
