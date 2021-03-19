# Copyright (C) 2019 - 2021 Richard Kemp
# $Id$
# -*- coding: utf-8; py-indent-offset:4 -*-

"""Polygon Datasource Module.

Provide:
    - Polygon Datasource Class
"""

__copyright__ = "Copyright 2019 - 2021 Richard Kemp"
__revision__ = "$Id$"
__all__ = [
    "Datasource",
]

from datetime import datetime
from typing import Dict

from mercury import Timeframe, Timeseries
from mercury.lib import Datasource as AbcDataSource

import pandas as pd

from polygon import RESTClient


TIMEFRAME_MAP = {
    Timeframe.M1: {"multiplier": 1, "timestamp": "minute"},
    Timeframe.M5: {"multiplier": 5, "timestamp": "minute"},
    Timeframe.M15: {"multiplier": 15, "timestamp": "minute"},
    Timeframe.M30: {"multiplier": 30, "timestamp": "minute"},
    Timeframe.H1: {"multiplier": 1, "timestamp": "minute"},
    Timeframe.H4: {"multiplier": 4, "timestamp": "hour"},
    Timeframe.D1: {"multiplier": 1, "timestamp": "day"},
    Timeframe.W1: {"multiplier": 1, "timestamp": "week"},
    Timeframe.MN: {"multiplier": 1, "timestamp": "month"},
}

PolygonInstrumentType = ["stock", "crypto", "forex"]


class Datasource(AbcDataSource):
    """polygon.io datasource provider.

    Load data from website polygon.

    Attributes:
        api_key (str): polygon API key

    Usage::

        >>> from Mercury_contrib.datasources import Polygon
        >>> datasource = Polygon('api_key')
        >>> dataframe = datasource.get_timeseries(
                from_date=datetime(2019, 12, 1, 9, 00, 00),
                to_date=datetime(2019, 12, 15, 23, 00, 00),
                instrument="MSFT",
                timeframe=Timeframe.M5,
            )
    """
    def __init__(self, api_key: str,
                 instrument_type: PolygonInstrumentType) -> None:
        """Class initialization.

        Args:
            api_key: polygon api key,
            instrument_type: the Polygon instrument type [forex, crypto, stock]
        """
        self.api_key = api_key

        if instrument_type not in PolygonInstrumentType:
            raise ValueError("Unsupported Polygon instrument type")

        self.instrument_type = instrument_type

    @property
    def colsmap(self) -> Dict[str, str]:
        """Columns mapping dictionary.

        Provide a mapping to translate raw time series columns name
        to standardized naming convention.

        Expect standard names like "open", "high", "low", "close", "adj_close"
        and "volume".
        """
        return {
            "1. open": "open",
            "2. high": "high",
            "3. low": "low",
            "4. close": "close",
            "5. volume": "volume",
        }

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
        if timeframe is Timeframe.S:
            raise ValueError("S interval not supported")

        multiplier = TIMEFRAME_MAP[timeframe]["multiplier"]
        timestamp = TIMEFRAME_MAP[timeframe]["timestamp"]
        from_date = datetime.strftime(from_date, "%Y-%m-%d")
        to_date = datetime.strftime(to_date, "%Y-%m-%d")

        with RESTClient(self.api_key) as client:
            resp = client.stocks_equities_aggregates(instrument,
                                                     multiplier, timestamp,
                                                     from_date, to_date)
            data = pd.DataFrame(resp.results)

        return Timeseries(instrument, timeframe, data)
