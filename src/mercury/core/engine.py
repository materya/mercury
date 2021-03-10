# Copyright (C) 2019 - 2021 Richard Kemp
# $Id$
# -*- coding: utf-8; py-indent-offset:4 -*-

"""Mercury Engine Module."""

from __future__ import annotations


__copyright__ = "Copyright 2019 - 2021 Richard Kemp"
__revision__ = "$Id$"
__all__ = [
    "Engine",
]


import time
from datetime import datetime, timedelta
from typing import Type

from .broker import Broker
from .strategy import Strategy
from .timeseries import Timeframe
from ..lib import BaseClass


class Engine(BaseClass):
    """Engine."""
    def __init__(self, *, broker: Broker, strategy: Type[Strategy]) -> None:
        """Initialize."""
        self.broker = broker
        self.strategy = strategy
        self.candles = None

    @property
    def next_time(self) -> datetime:
        """Provide the datetime when the next tick should happen.

        Based on the current candle processed and the timeframe.
        """
        offset = 60  # Maybe make a parameter out of this, depending on broker
        return (self.candles.current["date"] +
                timedelta(seconds=self.timeframe.value + offset))

    def _run_loop(self) -> None:
        """Main Engine loop.

        The loop is triggered once the engine has been started.
        """
        while True:
            self.__logger.debug("- tick -")
            self.strategy.current = self.candles.current
            self.strategy.time = self.candles.current["date"].time()

            self.strategy.tick()

            self.__logger.debug(f"next check at {self.next_time}")
            sleep_duration = (self.next_time - datetime.now()).total_seconds()
            time.sleep(int(round(sleep_duration)))

            self.increment_candles()

    def increment_candles(self) -> None:
        """Increment candles with the last available from the broker."""
        while True:
            candle = self.broker.get_last_candle(self.instrument,
                                                 self.timeframe)
            try:
                if candle.current["date"] != self.candles.current["date"]:
                    self.candles.append(candle)
                    break
            except KeyError as error:
                print("ERROR", error)
                pass

            time.sleep(1)

    def start(self, *, instrument: str, timeframe: Timeframe,
              warmup: int = 1) -> None:
        """Start the engine."""
        self.warmup = warmup
        self.timeframe = timeframe
        self.instrument = instrument

        now = datetime.now()
        delta = timedelta(seconds=self.timeframe.value * self.warmup)

        self.candles = self.broker._api_get_candles(self.instrument,
                                                    self.timeframe,
                                                    start_date=(now - delta),
                                                    end_date=now)
        self.strategy = self.strategy(self.broker, self.candles)

        self._run_loop()
