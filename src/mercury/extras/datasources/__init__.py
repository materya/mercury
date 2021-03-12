# Copyright (C) 2019 - 2021 Richard Kemp
# $Id$
# -*- coding: utf-8; py-indent-offset:4 -*-

"""Mercury Datasources Extras Module."""

__copyright__ = "Copyright 2019 - 2021 Richard Kemp"
__revision__ = "$Id$"
__all__ = [
    "AlphaVantage",
    "CSV",
    "Polygon",
    "Quandl",
]


from .alphavantage import AlphaVantage
from .csv import CSV
from .polygon import Polygon
from .quandl import Quandl

# TODO:
# iex
# polygon.io
# quantopian
# yahoo
