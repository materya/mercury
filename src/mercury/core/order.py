# Copyright (C) 2019 - 2021 Richard Kemp
# $Id$
# -*- coding: utf-8; py-indent-offset:4 -*-

"""Mercury Order Module."""

from __future__ import annotations


__copyright__ = "Copyright 2019 - 2021 Richard Kemp"
__revision__ = "$Id$"
__all__ = [
    "Order",
    "OrderAction",
    "OrderType",
    "OrderStatus",
]


from datetime import datetime
from enum import Enum

from ..lib import BaseClass


class OrderType(Enum):
    """Order type."""
    OPEN = "OPEN"
    PENDING = "PENDING"
    CLOSE = "CLOSE"
    MODIFY = "MODIFY"
    DELETE = "DELETE"


class OrderAction(Enum):
    """Valid order actions."""
    BUY = "BUY"
    SELL = "SELL"
    BUY_LIMIT = "BUY_LIMIT"
    SELL_LIMIT = "SELL_LIMIT"
    BUY_STOP = "BUY_STOP"
    SELL_STOP = "SELL_STOP"


class OrderStatus(Enum):
    """Status an order can have."""
    INITIAL = 0
    SUBMITTED = 1
    ACCEPTED = 2
    CANCELLED = 3
    PARTIALLY_FILLED = 4
    FILLED = 5
    REJECTED = 6


class Order(BaseClass):
    """Order.

    TODO: Doc here
    """
    def __init__(self, action: OrderAction, price: int, volume: int, *,
                 instrument: str, position_id: str = None,
                 or_id: str = None, creation_date: datetime = datetime.now(),
                 expiration_date: datetime = None, tp: float = None,
                 sl: float = None, raw: dict = None) -> None:
        """Initialize."""
        self.action = action
        self.price = price
        self.volume = volume
        self.instrument = instrument
        self.position_id = position_id
        self.id = or_id
        self.creation_date = creation_date
        self.expiration_date = expiration_date
        self.tp = tp
        self.sl = sl
        self._raw = raw
