# Copyright (C) 2019 - 2021 Richard Kemp
# $Id$
# -*- coding: utf-8; py-indent-offset:4 -*-

"""Oanda Broker implementation Module."""

from __future__ import annotations

__copyright__ = "Copyright 2019 - 2021 Richard Kemp"
__revision__ = "$Id$"
__all__ = [
    "Oanda",
]


from datetime import datetime
from functools import reduce
from typing import List

from mercury import (Account, AccountType, Broker, CurrencyCode, OrderAction,
                     Position, PositionStatus, PriceType,
                     TimeFrame, TimeSeries)
from mercury.lib import Client

from oandapyV20 import API
from oandapyV20.endpoints import accounts, instruments

import pandas as pd


class Oanda(Broker):
    """Oanda Broker."""
    def __init__(self, *, account_id: str, login: str, password: str,
                 api_key: str, is_paper: bool = False, **kwargs) -> None:
        """Initialize."""
        self._api_key = api_key

        super().__init__("Oanda")

    @property
    def _client(self) -> Client:
        client = API(self._token)
        return client

    def _api_fees(self) -> float:
        return 0.0

    def _api_auth(self) -> None:
        pass

    def _api_get_account(self, account_id: str = None) -> Account:
        endpoint = accounts.AccountDetails(account_id)
        # TODO: try catch connection error here
        self._client.request(endpoint)
        raw_account = endpoint.response["account"]
        account_type = AccountType.MARGIN \
            if float(raw_account["marginRate"]) > 0 \
            else AccountType.CASH
        self.account = Account(currency=raw_account["currency"],
                               balance=raw_account["balance"],
                               account_type=account_type,
                               margin=float(raw_account["marginRate"]))

    def _api_get_candles(self, instrument: str, timeframe: TimeFrame, *,
                         start_date: datetime, end_date: datetime = None,
                         **kwargs) -> TimeSeries:
        endpoint = instruments.InstrumentsCandles(instrument=instrument,
                                                  params=kwargs)
        # TODO: make a standard request try/catch class internal method
        # TODO: validate mandatory params
        self._client.request(endpoint)
        data = endpoint.response
        init_candles = {"date": [], "open": [], "high": [], "low": [],
                        "close": [], "volume": []}

        def reduce_candles(candles, candle):
            candles["open"].append(candle["mid"]["o"])
            candles["high"].append(candle["mid"]["h"])
            candles["low"].append(candle["mid"]["l"])
            candles["close"].append(candle["mid"]["c"])
            candles["volume"].append(candle["volume"])
            return candles
        candles = reduce(reduce_candles, data["candles"], init_candles)

        return TimeSeries(instrument=instrument,
                          timeframe=timeframe,
                          dataframe=pd.DataFrame(candles))

    def _api_get_positions(self, *args,
                           status: PositionStatus = None) -> List(Position):
        return None

    def _api_get_market_price(self, instrument: str,
                              price_type: PriceType) -> float:
        return None

    def _api_submit_order(self, action: OrderAction, size: int, *,
                          price: float = None, currency: CurrencyCode = None,
                          instrument: str = None,
                          sl: float = None, tp: float = None) -> str:
        pass
