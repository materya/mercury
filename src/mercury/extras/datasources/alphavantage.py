# Copyright (C) 2019 - 2021 Richard Kemp
# $Id$
# -*- coding: utf-8; py-indent-offset:4 -*-

"""AlphaVantage DataSource Module.

Provide:
    - AlphaVantage DataSource Class
"""

__copyright__ = "Copyright 2019 - 2021 Richard Kemp"
__revision__ = "$Id$"
__all__ = [
    "AlphaVantage",
]

from datetime import datetime
from typing import Dict

from alpha_vantage.timeseries import TimeSeries as AVTimeSeries

from mercury import TimeFrame, TimeSeries
from mercury.lib import DataSource


class AlphaVantage(DataSource):
    """alphavantage.com datasource provider.

    Load data from website alphavantage.

    Attributes:
        api_key (str): alphavantage API key

    Usage::

        >>> from Mercury_contrib.datasources import AlphaVantage
        >>> datasource = AlphaVantage('api_key')
        >>> dataframe = datasource.get_timeseries(
                from_date=datetime(2019, 12, 1, 9, 00, 00),
                to_date=datetime(2019, 12, 15, 23, 00, 00),
                instrument="MSFT",
                timeframe=TimeFrame.M5,
            )
    """
    def __init__(self, api_key: str) -> None:
        """Class initialization.

        Args:
            api_key: alphavantage api key
        """
        self.api_key = api_key
        self.ts = AVTimeSeries(key=api_key, output_format="pandas",
                               indexing_type="date")

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
                       instrument: str, timeframe: TimeFrame) -> TimeSeries:
        """Retrieve a given timeseries from the datasource.

        Args:
            from_date: timeseries starting date.
            to_date: timeseries last date.
            instrument: target instrument.
            timeframe: target timeframe.

        Returns:
            An Mercury TimeSeries.

        Raises:
            IndexError: The requested time range cannot be satisfied.
        """
        if timeframe is TimeFrame.H4:
            raise ValueError("H4 interval not supported")

        interval = int(timeframe.value / 60)
        if interval <= 60:
            data, meta_data = self.ts.get_intraday(symbol=instrument,
                                                   interval=f"{interval}min",
                                                   outputsize="full")
        if timeframe is TimeFrame.D1:
            data, meta_data = self.ts.get_daily_adjusted(symbol=instrument,
                                                         outputsize="full")
        if timeframe is TimeFrame.W1:
            data, meta_data = self.ts.get_weekly_adjusted(symbol=instrument)
        if timeframe is TimeFrame.MN:
            data, meta_data = self.ts.get_monthly_adjusted(symbol=instrument)

        return TimeSeries(instrument, timeframe, data)
