# Copyright (C) 2019 - 2021 Richard Kemp
# $Id$
# -*- coding: utf-8; py-indent-offset:4 -*-

"""Polygon datasource Tests."""

__copyright__ = "Copyright 2019 - 2021 Richard Kemp"
__revision__ = "$Id$"

from datetime import datetime

from mercury import Timeframe, Timeseries

from mercury.extras.datasources.polygon import Datasource

from pandas import DataFrame

import pytest

# API_KEY = os.environ['POLYGON_API_KEY']
# API_KEY = 'TEST'


@pytest.fixture
def datasource():
    return Datasource(API_KEY, "stock")


class TestInstanciation():
    def test_valid_key(self, datasource):
        assert datasource

class TestGetMethod():
    @pytest.mark.online
    def test_invalid_interval(self, datasource):
        with pytest.raises(ValueError) as error:
            assert datasource.get_timeseries(
                from_date=datetime(2019, 12, 1, 9, 00, 00),
                to_date=datetime(2019, 12, 2, 23, 00, 00),
                instrument="AAPL",
                timeframe=Timeframe.S)
        message = str(error.value)
        assert message == "S interval not supported"

    @pytest.mark.online
    def test_invalid_instrument_type(self):
        with pytest.raises(ValueError) as error:
            datasource = Datasource(API_KEY, "stuck")
            assert datasource.get_timeseries(
                from_date=datetime(2019, 12, 1, 9, 00, 00),
                to_date=datetime(2019, 12, 2, 23, 00, 00),
                instrument="AAPL",
                timeframe=Timeframe.M5)
        message = str(error.value)
        assert message == "Unsupported Polygon instrument type"

    @pytest.mark.online
    def test_intraday_stock_data(self, datasource):
        instrument = "AAPL"
        timeframe = Timeframe.M5
        ts = datasource.get_timeseries(
            from_date=datetime(2019, 12, 1, 9, 00, 00),
            to_date=datetime(2019, 12, 2, 23, 00, 00),
            instrument=instrument,
            timeframe=timeframe)
        assert isinstance(ts, Timeseries)
        assert ts.instrument is instrument
        assert ts.timeframe is timeframe
        assert isinstance(ts.data, DataFrame)

    @pytest.mark.online
    def test_intraday_forex_data(self, datasource):
        instrument = "C:EURUSD"
        timeframe = Timeframe.M5
        ts = datasource.get_timeseries(
            from_date=datetime(2019, 12, 1, 9, 00, 00),
            to_date=datetime(2019, 12, 2, 23, 00, 00),
            instrument=instrument,
            timeframe=timeframe)
        assert isinstance(ts, Timeseries)
        assert ts.instrument is instrument
        assert ts.timeframe is timeframe
        assert isinstance(ts.data, DataFrame)

    @pytest.mark.online
    def test_intraday_crypto_data(self, datasource):
        instrument = "X:BTCUSD"
        timeframe = Timeframe.M5
        ts = datasource.get_timeseries(
            from_date=datetime(2019, 12, 1, 9, 00, 00),
            to_date=datetime(2019, 12, 2, 23, 00, 00),
            instrument=instrument,
            timeframe=timeframe)
        assert isinstance(ts, Timeseries)
        assert ts.instrument is instrument
        assert ts.timeframe is timeframe
        assert isinstance(ts.data, DataFrame)

    # @pytest.mark.online
    def test_daily_data(self, datasource):
        instrument = "MSFT"
        timeframe = Timeframe.D1
        ts = datasource.get_timeseries(
            from_date=datetime(2019, 12, 1, 9, 00, 00),
            to_date=datetime(2019, 12, 15, 23, 00, 00),
            instrument=instrument,
            timeframe=timeframe)
        assert isinstance(ts, Timeseries)
        assert ts.instrument is instrument
        assert ts.timeframe is timeframe
        assert isinstance(ts.data, DataFrame)

    @pytest.mark.online
    def test_weekly_data(self, datasource):
        instrument = "MSFT"
        timeframe = Timeframe.W1
        ts = datasource.get_timeseries(
            from_date=datetime(2019, 12, 1, 9, 00, 00),
            to_date=datetime(2019, 12, 15, 23, 00, 00),
            instrument=instrument,
            timeframe=timeframe)
        assert isinstance(ts, Timeseries)
        assert ts.instrument is instrument
        assert ts.timeframe is timeframe
        assert isinstance(ts.data, DataFrame)

    @pytest.mark.online
    def test_monthly_data(self, datasource):
        instrument = "MSFT"
        timeframe = Timeframe.MN
        ts = datasource.get_timeseries(
            from_date=datetime(2019, 12, 1, 9, 00, 00),
            to_date=datetime(2019, 12, 15, 23, 00, 00),
            instrument=instrument,
            timeframe=timeframe)
        assert isinstance(ts, Timeseries)
        assert ts.instrument is instrument
        assert ts.timeframe is timeframe
        assert isinstance(ts.data, DataFrame)
