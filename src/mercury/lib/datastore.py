# -*- coding: utf-8; py-indent-offset:4 -*-
# Copyright (C) 2019 - 2021 Richard Kemp

"""Mercury Datastore module.

Provide:
    - Datastore superclass
"""

from __future__ import annotations


__copyright__ = "Copyright 2019 - 2021 Richard Kemp"
__revision__ = "$Id$"
__all__ = [
    "Datastore",
]


from abc import abstractmethod

from pandas import DataFrame

from .baseclass import BaseMetaClass


class Datastore(metaclass=BaseMetaClass):
    """Datastore interface.

    A datastore is a storage dedicated for trading timeseries data,
    usually previously retrieve an stored from a datasource in order
    to avoid similar recurrent queries either because of performance or cost.
    """
    @abstractmethod
    def _connect(self) -> None:
        """Connect to the datastore.

        Will be automatically triggered during object initialization.
        """

    @abstractmethod
    def store(self, name: str, data: DataFrame, metadata: dict = {}) -> None:
        """Save a given new dataframe."""

    @abstractmethod
    def append(self, name: str, data: DataFrame) -> None:
        """Append data to an existing dataset."""

    @abstractmethod
    def get(self, name: str) -> DataFrame:
        """Retrieve a specific dataset."""
