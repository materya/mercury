# Copyright (C) 2019 - 2021 Richard Kemp
# $Id$
# -*- coding: utf-8; py-indent-offset:4 -*-

"""Mercury Backtest tools Module."""

from __future__ import annotations


__copyright__ = "Copyright 2019 - 2021 Richard Kemp"
__revision__ = "$Id$"
__all__ = [
    "BacktestBroker",
]

from .. import Broker
# from ..lib import InstrumentCandles


class MockBrokerApi():
    """Mock of a broker API class for backtesting simulation."""
    def __init__(self, token) -> None:
        super().__init__()
        self.token = token

    def set_orders(self) -> dict:
        """Get opened orders."""
        return {}

    def get_orders(self) -> dict:
        """Get opened orders."""
        return {}


class BacktestBroker(Broker):
    """Dummy Broker for backtesting."""
    def __init__(self, account) -> None:
        """Initialize."""
        super().__init__("BacktestBroker")
        self.account = account

    # def fees(self):
    #     return 0

    # def _connect(self):
    #     return MockBrokerAPI("dummy_token")

    # def get_account(self, account_id: str) -> Account:
    #     return self.account

    # def get_candles(self, instrument: str,
    # params: dict) -> InstrumentCandles:
    #     data = {
    #         "open": [1, 2, 3, 4, 5],
    #         "high": [1, 2, 3, 4, 5],
    #         "low": [1, 2, 3, 4, 5],
    #         "close": [1, 2, 3, 4, 5],
    #     }
    #     return InstrumentCandles(instrument=instrument, timeframe="H1",
    #                              dataframe=pd.DataFrame(data))

    # def get_positions(self, *args):
    #     return []

    # def open_position(self, direction: TradeType, size: int,
    #                   ptype: OrderType, *, level: float = None,
    #                   sl: float = None, tp: float = None) -> None:
    #     position = Position(size, datetime.datetime.now(), broker=self,
    #                         direction=direction, sl=sl, tp=tp)
    #     self._positions.append(position)
