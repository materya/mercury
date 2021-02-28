# Copyright (C) 2019 - 2021 Richard Kemp
# $Id$
# -*- coding: utf-8; py-indent-offset:4 -*-

"""SMA Crossover Strategy standalone Module."""

__copyright__ = "Copyright 2019 - 2021 Richard Kemp"
__revision__ = "$Id$"
__all__ = [
    "StrategySmaCrossOver",
]


from typing import Callable

from mercury import Indicator, OrderAction, PriceType, Strategy
from mercury.lib import crossover, crossunder

import talib


def sma(timeperiod: int) -> Callable:
    return lambda candles: talib.SMA(candles.close, timeperiod)


class StrategySmaCrossOver(Strategy):
    """Demo sample basic SMA Crossover strategy.

    This strategy is for demo purpose only and is very basic.
    It is highly suggested to not try to trade on a real account with it.
    """
    def setup(self) -> None:
        """Initialize the strategy."""
        self.add_indicator(Indicator("sma10", sma(10)))
        self.add_indicator(Indicator("sma30", sma(30)))

        self.set_factor()

    def set_factor(self) -> None:
        """Set the strategy multiplier factor."""
        self.factor = 1

    def tick(self) -> None:
        """Tick per tick strategy run."""
        positions = self.broker.positions

        instrument = self.candles.instrument
        currency = "EUR"

        if positions:
            if crossunder(self.sma10, self.sma30):
                print("current positions", positions)
                if len(positions) > 1:
                    raise Exception("only one pos. should be opened at a time")
                position = positions[0]
                self.broker._close_position(position)
        elif crossover(self.sma10, self.sma30):
            action = OrderAction.BUY
            price_type = PriceType.ASK
            price = self.broker._api_get_market_price(instrument, price_type)
            self.__logger.info(f"opening new BUY position at {price}")
            self.broker._api_submit_order(action, self.factor,
                                          price=price,
                                          currency=currency,
                                          instrument=instrument,
                                          sl=0.0, tp=0.0)
