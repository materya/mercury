# Copyright (C) 2019 - 2021 Richard Kemp
# $Id$
# -*- coding: utf-8; py-indent-offset:4 -*-

"""Mercury Strategy Module.

Provide:
    - Indicator Class
    - Strategy Interface
"""

from __future__ import annotations


__copyright__ = "Copyright 2019 - 2021 Richard Kemp"
__revision__ = "$Id$"
__all__ = [
    "Indicator",
    "Strategy",
]


from abc import ABCMeta, abstractmethod
from typing import Callable, List

import numpy as np

from ..core.broker import Broker
from ..core.timeseries import Timeseries
from ..lib import BaseClass


class Indicator(BaseClass):
    """An indicator to use in Strategy.

    TODO: doc here
    """
    def __init__(self, name: str, func: Callable, *,
                 plot: bool = True, overlay: bool = False,
                 color: str = None, scatter: bool = False) -> None:
        """Initialize."""
        self.name = name
        self._func = func
        self.params = {"plot": plot, "overlay": overlay,
                       "color": color, "scatter": scatter}
        self._data = np.array([])

    def __getitem__(self, index: int) -> float:
        """Override __getitem__."""
        return self._data[index]

    def __float__(self) -> float:
        """Override __float__."""
        try:
            value = float(self._data[-1])
        except (IndexError, KeyError):
            value = float("NaN")
        return value

    def __gt__(self, other: Indicator) -> bool:
        """Override __gt__."""
        return float(self) > float(other)

    def __ge__(self, other: Indicator) -> bool:
        """Override __ge__."""
        return float(self) >= float(other)

    def __lt__(self, other: Indicator) -> bool:
        """Override __lt__."""
        return float(self) < float(other)

    def __le__(self, other: Indicator) -> bool:
        """Override __le__."""
        return float(self) <= float(other)

    def __str__(self) -> str:
        """Override __str__."""
        return str(float(self))

    def apply(self, timeseries: Timeseries) -> None:
        """Run the indicator function against a timeseries and store it."""
        self._data = self._func(timeseries)

    def data(self) -> List[float]:
        """Return all computed values."""
        return self._data

    def previous(self, shift: int = 1) -> float:
        """Return previous value based on a shift."""
        try:
            value = self._data[-(1 + shift)]
        except IndexError:
            value = float("NaN")

        return value


class StrategyMeta(ABCMeta, type(BaseClass)):
    """Strategy metaclass wrapper.

    This trick is needed when you want to use more than one metaclass
    for a given class.
    """
    pass


class Strategy(metaclass=StrategyMeta):
    """Trading strategy base class.

    Extend this class and override methods
    `mercury.Strategy.setup` and
    `mercury.Strategy.tick` to define your own strategy.
    """
    def __init__(self, broker: Broker, timeseries: Timeseries) -> None:
        """Initialize."""
        self._indicators = {}
        self.broker = broker
        self.timeseries = timeseries
        self.setup()

    def __getattr__(self, name: str) -> Indicator:
        """Override __getattr__."""
        # TODO: do not recompute but move the indicator's cursor in some way
        # like for candles
        indicator = self._indicators[name]
        indicator.apply(self.timeseries)

        return indicator

    @abstractmethod
    def setup(self) -> None:
        """Initialize a strategy.

        TODO: doc here
        """

    @abstractmethod
    def tick(self) -> None:
        """Main runtime method, called when new data becomes available.

        This is the main method where strategy decisions are taken.

        If you extend composable strategies from `mercury.contrib.strategies`
        make sure to call:

            super().tick()
        """

    def add_indicator(self, indicator: Indicator) -> None:
        """Add an indicator in the strategy.

        TODO: write the doc here
        """
        self._indicators[indicator.name] = indicator
