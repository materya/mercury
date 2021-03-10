# -*- coding: utf-8; py-indent-offset:4 -*-
# Copyright (C) 2019 - 2021 Richard Kemp

"""Mercury Datasource module.

Provide:
    - Datasource Interface
"""

from __future__ import annotations


__copyright__ = "Copyright 2019 - 2021 Richard Kemp"
__revision__ = "$Id$"
__all__ = [
    "Datasource",
]


from abc import ABCMeta, abstractmethod, abstractproperty
from datetime import datetime
from typing import Dict


from ..core.timeseries import Timeframe, Timeseries


class Datasource(object, metaclass=ABCMeta):
    """Datasource Interface.

    A datasource is a way to retrieve fresh trading data (typically OHLC) from
    a specific source.
    """
    @abstractproperty
    def colsmap(self) -> Dict[str, str]:
        """Columns mapping dictionary.

        Provide a mapping to translate raw time series columns name
        to Mercury Datasource naming convention.

        Expect standard names like "open", "high", "low", "close", "adj_close"
        and "volume".
        """

    @abstractmethod
    def get_timeseries(self, from_date: datetime, to_date: datetime,
                       instrument: str, timeframe: Timeframe) -> Timeseries:
        """Retrieve a given timeseries from the datasource.

        Args:
            from_date: timeseries starting date.
            to_date: timeseries last date.
            instrument: target instrument.
            timeframe: target timeframe.

        Returns:
            An Mercury Timeseries.

        Raises:
            IndexError: The requested time range cannot be satisfied.
        """
