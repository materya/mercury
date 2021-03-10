# Copyright (C) 2019 - 2021 Richard Kemp
# $Id$
# -*- coding: utf-8; py-indent-offset:4 -*-

"""CSV Datasource Module.

Provide:
    - CSV Datasource Class
"""


from __future__ import annotations


__copyright__ = "Copyright 2019 - 2021 Richard Kemp"
__revision__ = "$Id$"
__all__ = [
    "Datasource",
]


from typing import Dict

from mercury import Timeframe, Timeseries
from mercury.lib import Datasource as AbcDatasource

import pandas as pd
from pandas.core.indexes.datetimes import DatetimeIndex


class Datasource(AbcDatasource):
    """Simple CSV datasource provider.

    Load data from a .csv file.

    Attributes:
        file (str): csv file location.
        colsmap (dict): dict mapping of columns name.
        instrument (str): instrument codename reference.
        timeframe (Timeframe): data timeframe.

    Usage::

        >>> from Mercury import Timeframe
        >>> from Mercury.contrib.datasources import CSV
        >>> colsmap = {
            "Date Time": "date",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume",
        }
        >>> datasource = CSV('./some/file.csv', colsmap, "Date Time",
        "EURUSD", Timeframe.H1)
        >>> dataframe = datasource.get_source()
    """
    def __init__(self, filepath: str, colsmap: Dict[str, str],
                 index: str, instrument: str, timeframe: Timeframe) -> None:
        """Class initializater.

        Args:
            filepath: target csv file location.
            colsmap: dict mapping of the csv columns name to a standard naming
                convention uses by the library.
            index: (not mapped) name of the column to use as index.
            instrument (str): instrument codename reference.
            timeframe (Timeframe): data timeframe.
        """
        self.file = filepath
        self._colsmap = colsmap
        self.index = index
        self.instrument = instrument
        self.timeframe = timeframe

        try:
            dataframe = pd.read_csv(filepath, index_col=index,
                                    usecols=colsmap and colsmap.keys(),
                                    parse_dates=True,
                                    infer_datetime_format=True)
            if (type(dataframe.index) is not DatetimeIndex):
                raise ValueError(f"'{index}' column is not a valid datetime")
            dataframe.rename(columns=colsmap, inplace=True)
            dataframe.index.names = [colsmap[index]]
            self.data = dataframe
        except ValueError as error:
            if str(error) == f"'{index}' is not in list":
                raise ValueError(f"Index column '{index}' does not exist") \
                    from None
            raise error

    @property
    def colsmap(self) -> Dict[str, str]:
        """Columns mapping dictionary.

        Provide a mapping to translate raw time series columns name
        to standardized naming convention.

        Expect standard names like "open", "high", "low", "close", "adj_close"
        and "volume".
        """
        return self._colsmap

    def get_timeseries(self) -> Timeseries:
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
        return Timeseries(self.instrument, self.timeframe, self.data)
