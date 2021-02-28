# Copyright (C) 2019 - 2021 Richard Kemp
# $Id$
# -*- coding: utf-8; py-indent-offset:4 -*-

"""Mercury Backtest Module."""

__copyright__ = "Copyright 2019 - 2021 Richard Kemp"
__revision__ = "$Id$"
__all__ = [
    "Simulator",
]


# from .broker import BacktestBroker
from .. import Strategy
from ..lib import BaseClass, DataSource, DataStore


class Simulator(BaseClass):
    """Backtest strategy simulation."""
    def __init__(self, strategy: Strategy, *, datastore: DataStore,
                 datasource: DataSource = None, warmup: int = 1) -> None:
        """Initialize."""
        # some sanity checks
        if datasource and not isinstance(datasource, DataSource):
            raise TypeError("`datasource` must be a `DataSource` subclass")
        if not isinstance(datastore, DataStore):
            raise TypeError("`datastore` must be a `DataStore` subclass")

        # self.broker = BacktestBroker(account)
        self.strategy = strategy
        # self.candles = candles
        self.warmup = warmup

    def run(self) -> None:
        """Execute the backtest."""
        strategy = self.strategy(self.broker, self.candles)
        # start = 1 + max((np.isnan(indicator).argmin()
        #                  for _, indicator in indicator_attrs), default=0)
        # test = max((np.isnan(indicator).argmin()
        #             for _, indicator in strategy._indicators.items()))
        for i in range(self.warmup, len(self.candles)):
            self.candles.set_cursor(i)

            # Aliases to use inside the strategy
            strategy.current = self.candles.current
            strategy.time = self.candles.current.get("date").time()

            strategy.tick()

    def optimize(self) -> None:
        """Run the backtest several times with different params.

        Goal is to find the best values for each param tested and suggest them
        for a real run and get the most out of the strategy backtested.
        """
