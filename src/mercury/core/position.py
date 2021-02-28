# Copyright (C) 2019 - 2021 Richard Kemp
# $Id$
# -*- coding: utf-8; py-indent-offset:4 -*-

"""Mercury Positions Module."""

from __future__ import annotations


__copyright__ = "Copyright 2019 - 2021 Richard Kemp"
__revision__ = "$Id$"
__all__ = [
    "Position",
    "PositionType",
    "PositionStatus",
]


from datetime import datetime
from enum import Enum

from ..lib import BaseClass


class PositionType(Enum):
    """Position Type."""
    BUY = "BUY"
    SELL = "SELL"


class PositionStatus(Enum):
    """Position Status."""
    OPENED = "OPENED"
    CLOSED = "CLOSED"


class Position(BaseClass):
    """Replicate a broker position."""
    def __init__(self, direction: PositionType, volume: int, *,
                 status: PositionStatus = PositionStatus.OPENED,
                 instrument: str,
                 pos_id: str = None, reference_order_id: str = None,
                 open_price: float, open_date: datetime = datetime.now(),
                 close_price: float = None, close_date: datetime = None,
                 tp: float = None, sl: float = None,
                 profit: float = 0.0, spread: float = 0.0, taxes: float = 0.0,
                 raw: dict = None) -> None:
        """Initialize."""
        self.type = direction
        self.volume = volume
        self.status = status
        self.instrument = instrument
        self.id = pos_id
        self.reference_order_id = reference_order_id
        self.open_price = open_price
        self.open_date = open_date
        self.close_price = close_price
        self.close_date = close_date
        self.tp = tp
        self.sl = sl
        self.profit = profit
        self.spread = spread
        self.taxes = taxes
        self._raw = raw
