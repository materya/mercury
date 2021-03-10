# Copyright (C) 2019 - 2021 Richard Kemp
# $Id$
# -*- coding: utf-8; py-indent-offset:4 -*-

"""Quandl Datasource Module.

Provide:
    - Quandl Datasource Class
"""

__copyright__ = "Copyright 2019 - 2021 Richard Kemp"
__revision__ = "$Id$"
__all__ = [
    "Datasource",
]

from datetime import datetime
from typing import Dict

from mercury import Timeframe, Timeseries
from mercury.lib import Datasource as AbcDatasource

import quandl


class Datasource(AbcDatasource):
    """quandl.com datasource provider.

    Attributes:
        api_key (str): Quandl API key

    Usage::

        >>> from Mercury_contrib.datasources import Quandl
        >>> datasource = Quandl('api_key')
        >>> dataframe = datasource.get_timeseries(
                from_date=datetime(2019, 12, 1, 9, 00, 00),
                to_date=datetime(2019, 12, 15, 23, 00, 00),
                instrument="MSFT",
                timeframe=Timeframe.M5,
            )
    """
    def __init__(self, api_key: str) -> None:
        """Class initializer.

        Args:
            api_key: Quandl api key
        """
        self.api_key = api_key

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
        data = quandl.get(instrument)

        return Timeseries(instrument, timeframe, data)
