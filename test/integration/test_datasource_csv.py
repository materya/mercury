# Copyright (C) 2019 - 2021 Richard Kemp
# $Id$
# -*- coding: utf-8; py-indent-offset:4 -*-

"""CSV datasource Tests."""

__copyright__ = "Copyright 2019 - 2021 Richard Kemp"
__revision__ = "$Id$"

from os.path import dirname, join

from mercury import TimeFrame, TimeSeries

from mercury.extras.datasources import CSV

from pandas import DataFrame

import pytest


FILE = join(dirname(__file__), "../data/EURUSD.csv")
COLSMAP = {
    "Date Time": "date",
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Close": "close",
    # "Ajd. Close": "adj_close",
    "Volume": "volume",
}
INDEX = "Date Time"
INSTRUMENT = "EURUSD"
TIMEFRAME = TimeFrame.H1


class TestInstanciation():
    def test_invalid_file(self):
        with pytest.raises(FileNotFoundError):
            assert CSV("./unknown/location/file.csv", COLSMAP, INDEX,
                       INSTRUMENT, TIMEFRAME)

    def test_invalid_index(self):
        bad_index = "foo"
        with pytest.raises(ValueError) as error:
            assert CSV(FILE, COLSMAP, bad_index, INSTRUMENT, TIMEFRAME)
        message = str(error.value)
        assert message == f"Index column '{bad_index}' does not exist"

    def test_not_datetime_index(self):
        bad_index = "Volume"
        with pytest.raises(ValueError) as error:
            assert CSV(FILE, COLSMAP, bad_index, INSTRUMENT, TIMEFRAME)
        message = str(error.value)
        assert message == f"'{bad_index}' column is not a valid datetime"

    def test_valid_instanciation(self):
        assert CSV(FILE, COLSMAP, INDEX, INSTRUMENT, TIMEFRAME)


class TestColsmapProperty():
    def test_value(self):
        ds = CSV(FILE, COLSMAP, INDEX, INSTRUMENT, TIMEFRAME)
        assert ds.colsmap is COLSMAP


class TestGetMethod():
    def test_get_successful(self):
        ds = CSV(FILE, COLSMAP, INDEX, INSTRUMENT, TIMEFRAME)
        ts = ds.get_timeseries()
        assert isinstance(ts, TimeSeries)
        assert ts.instrument is INSTRUMENT
        assert ts.timeframe is TIMEFRAME
        assert isinstance(ts.data, DataFrame)

    # def test_get_existing_range_data(self):
    #     ds = CSV(FILE, COLSMAP, INDEX)
    #     df = ds.get()
    #     assert isinstance(df, DataFrame)

    # def test_get_invalid_range_data(self):
    #     df = datasource.get(from_date=datetime(2019, 1, 1, 9, 00, 00),
    #                         to_date=datetime(2019, 2, 1, 23, 00, 00),
    #                         instrument='EURUSD',
    #                         timeframe=TimeFrame.H1)
