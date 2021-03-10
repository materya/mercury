# Copyright (C) 2019 - 2021 Richard Kemp
# $Id$
# -*- coding: utf-8; py-indent-offset:4 -*-

"""Mercury Broker module.

TODO: docs goes here
"""

from __future__ import annotations

__copyright__ = "Copyright 2019 - 2021 Richard Kemp"
__revision__ = "$Id$"
__all__ = [
    "Broker",
    "CurrencyCode",
    "LotSize",
    "PriceType",
]


import time
from abc import abstractmethod
from datetime import datetime, timedelta
from enum import Enum
from typing import List, TypeVar


from . import Account
from .order import Order, OrderAction
from .position import Position, PositionStatus, PositionType
from .timeseries import Timeframe, Timeseries
from ..lib import BaseMetaClass, Client
from ..lib.exceptions import ConnectionLostError


T = TypeVar("T")


class CurrencyCode(Enum):
    """Common currency codename."""
    EUR = "EUR"
    USD = "USD"
    CAD = "CAD"
    GBP = "GBP"
    JPY = "JPY"


class LotSize(Enum):
    """Lotsize Enum units."""
    INTERBANK = 1000000
    STANDARD = 100000
    MINI = 10000
    MICRO = 1000
    NANO = 100


class PriceType(Enum):
    """Trading current price types."""
    ASK = 0  # BUY
    BID = 1  # SELL
    LAST = 2


class Broker(metaclass=BaseMetaClass):
    """Broker abstract interface class.

    This is a meta class and it should not be call directly
    superclass it instead.
    """
    # TODO: margin call limit
    def __init__(self, name: str, account_id: str = None) -> None:
        """Class Initializer."""
        self.name = name
        self.account_id = account_id
        self._positions = []

        # Get the client for the whole session
        self.__client = self._client

        self.__client.connect()
        self._api_auth()

        self.account = self._api_get_account(self.account_id)

    #
    # ABSTRACT METHODS
    #
    # Implementation of all mandatories broker's API routes/methods
    #
    @property
    @abstractmethod
    def _client(self) -> Client:
        """Returns a subclass of Client, all requests will be passed to."""

    @abstractmethod
    def _api_fees(self):
        """Calculate the broker interest fees for a closed position."""

    @abstractmethod
    def _api_auth(self) -> None:
        """Implement the broker authentication method."""

    @abstractmethod
    def _api_get_account(self, account_id: str = None) -> Account:
        """Implement the broker's method to get the account details."""

    @abstractmethod
    def _render_order(self, raw: dict) -> Order:
        """Implement a translator for a raw order from the broker API."""

    @abstractmethod
    def _render_position(self, raw: dict) -> Position:
        """Implement a translator for a raw position from the broker API."""

    @abstractmethod
    def _api_get_candles(self, instrument: str, timeframe: Timeframe, *,
                         start_date: datetime, end_date: datetime = None,
                         **kwargs) -> Timeseries:
        """Implement the broker's method to get instrument candles values."""

    @abstractmethod
    def _api_get_market_price(self, instrument: str,
                              price_type: PriceType) -> float:
        """Return the current market price."""

    @abstractmethod
    def _api_submit_order(self, action: OrderAction, size: int, *,
                          price: float = None, currency: CurrencyCode = None,
                          instrument: str = None,
                          sl: float = None, tp: float = None) -> str:
        """Implement the broker"s method to submit an order.

        must return an order id.
        """

    @abstractmethod
    def _api_get_positions(self, *args,
                           status: PositionStatus = None) -> List[Position]:
        """Implement the broker's method to get current positions."""

    @abstractmethod
    def _api_close_position(self, position: Position, level: float) -> bool:
        """Implement the broker's method to close a position."""

    #
    # PROPERTIES
    #
    @property
    def is_long(self) -> bool:
        """Indicate whether there's open long positions."""
        return any(position.type == PositionType.BUY
                   for position in self._positions)

    @property
    def is_short(self) -> bool:
        """Indicate whether there's open short positions."""
        return any(position.type == PositionType.SELL
                   for position in self._positions)

    @property
    def positions(self) -> bool:
        """Return all current positions."""
        return self._positions

    #
    # FUNCTIONAL METHODS
    #
    # These are the actual methods used by components, they all depend from
    # the abstract ones from any subclass.
    #

    def _sync_positions(self) -> None:
        """Get positions live from the broker and refresh the local cache."""
        self._positions = self._api_get_positions()

    # def positions(self, refresh: bool = True) -> List(Positions):
    #     """return all current open positions"""
    #     refresh and self._sync_positions()
    #     return self._positions

    def request(self, payload: T, **opts) -> T:
        """Emit a request to the client.

        The client is responsible to handle the payload type
        This method is able to try to reconnect if for any reason it loses the
        connection with the server.
        """
        try:
            return self.__client.request(payload, **opts)
        except ConnectionLostError:
            self.__logger.warning("connection lost, retrying...")
            self.__client.connect()
            self._api_auth()
            return self.__client.request(payload, **opts)

    def get_last_candle(self, instrument: str,
                        timeframe: Timeframe) -> Timeseries:
        """Return the last available candle.

        This method uses the internal abstract method `_api_get_candles`
        to provide this data.
        """
        start_date = (datetime.now() - timedelta(seconds=timeframe.value))
        retry = 0.5

        while True:
            candles = self._api_get_candles(instrument, timeframe,
                                            start_date=start_date)
            if len(candles):
                break

            time.sleep(retry)
            retry += retry

        return candles

    def long_positions(self, refresh: bool = False) -> List[Position]:
        """Return all current long open positions."""
        refresh and self._sync_positions()
        return [p for p in self._positions
                if p.type == PositionType.BUY]

    def short_positions(self, refresh: bool = False) -> List[Position]:
        """Return all current short open positions."""
        refresh and self._sync_positions()
        return [p for p in self._positions
                if p.type == PositionType.SELL]

    def close(self, position: Position, level: float) -> None:
        """Close a currently open position."""
        self._api_close_position(position, level)

    def __str__(self) -> str:
        """Override __str__."""
        return self.name

    def __repr__(self) -> str:
        """Override __repr__."""
        return "<Broker: {}>".format(self.name)
