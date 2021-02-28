# -*- coding: utf-8; py-indent-offset:4 -*-
# Copyright (C) 2019 - 2021 Richard Kemp

"""Mercury FlexArray module.

Provide

- FlexArray
"""

from __future__ import annotations


__copyright__ = "Copyright 2019 - 2021 Richard Kemp"
__revision__ = "$Id$"
__all__ = [
    "FlexArray",
]


import numpy as np

import pandas as pd

from .baseclass import BaseClass

# TODO: to improve based on backtesting.py/backtesting/_util.py stuff


class FlexArray(BaseClass):
    """Wrap pandas DataFrame for specific needs in Mercury.

    TODO: doc here
    """
    def __init__(self, dataframe: pd.DataFrame) -> None:
        """Initialize a mercury DataFrame from a pandas DataFrame."""
        # TODO: make cursor private read-only (see double undescrore)
        # https://stackoverflow.com/a/39716001/3612177
        self.dataframe = dataframe
        self._cache = {}
        self._cursor = None
        self._reindex()

    def __getitem__(self, item: str) -> np.ndarray:
        """Override __getitem__."""
        return getattr(self, item)

    def __getattr__(self, item: str) -> np.ndarray:
        """Override __getattr__."""
        try:
            return self._get_slice(item)
        except KeyError:
            raise KeyError("Column '{}' not in data".format(item)) from None

    # def __repr__(self) -> str:
    #     return ("<DataFrame: {instrument} {timeframe}>"
    #            .format(instrument=self.instrument, timeframe=self.timeframe))

    # __str__ = __repr__

    def __len__(self) -> int:
        """Override __len__."""
        return self._cursor

    def _reindex(self) -> None:
        """Rebuild internal index from the original dataframe."""
        self._cache.clear()
        self._cursor = len(self.dataframe)
        self._data = {col: np.array(array)
                      for col, array in self.dataframe.items()}
        self._data["index"] = self.dataframe.index.copy()

    def _get_slice(self, key) -> np.ndarray:
        """Extract an array subset based on DataFrame._cursor value.

        TODO: doc here
        """
        if self._cache.get(key) is None:
            key = "index" if key == self._data.get("index").name else key
            self._cache[key] = self._data[key][:self._cursor]
        return self._cache.get(key)

    def set_cursor(self, cursor) -> None:
        """Set the internal cursor value to shift the subset representation.

        TODO: doc here
        """
        self._cursor = cursor
        self._cache.clear()

    def append(self, array: FlexArray) -> None:
        """Append another array to the current one."""
        # TODO: ensure both dataframe are compatible
        # index_name = self._data.get("index").name
        self.dataframe = self.dataframe.append(array.dataframe)
        self._reindex()

    @property
    def current(self) -> dict:
        """Return the last candle values.

        TODO: doc here
        """
        values = {key: data[self._cursor - 1]
                  for key, data in self._data.items()}
        values[self._data.get("index").name] = values.pop("index")

        return values
