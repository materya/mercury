# Copyright (C) 2019 - 2021 Richard Kemp
# $Id$
# -*- coding: utf-8; py-indent-offset:4 -*-

"""Alphavantage datasource Tests."""

__copyright__ = "Copyright 2019 - 2021 Richard Kemp"
__revision__ = "$Id$"

from datetime import datetime

from mercury import TimeFrame, TimeSeries

from mercury.extras.datasources.alphavantage import DataSource

from pandas import DataFrame

import pytest

# API_KEY = os.environ['ALPHAVANTAGE_API_KEY']
API_KEY = 'TEST'


@pytest.fixture
def datasource():
    return DataSource(API_KEY)


class TestInstanciation():
    def test_valid_key(self, datasource):
        assert datasource


class TestGetMethod():
    @pytest.mark.online
    def test_invalid_interval(self, datasource):
        with pytest.raises(ValueError) as error:
            assert datasource.get_timeseries(
                from_date=datetime(2019, 12, 1, 9, 00, 00),
                to_date=datetime(2017, 12, 15, 23, 00, 00),
                instrument="MSFT",
                timeframe=TimeFrame.H4)
        message = str(error.value)
        assert message == "H4 interval not supported"

    @pytest.mark.online
    def test_intraday_data(self, datasource):
        instrument = "MSFT"
        timeframe = TimeFrame.M5
        ts = datasource.get_timeseries(
            from_date=datetime(2019, 12, 1, 9, 00, 00),
            to_date=datetime(2019, 12, 15, 23, 00, 00),
            instrument=instrument,
            timeframe=timeframe)
        assert isinstance(ts, TimeSeries)
        assert ts.instrument is instrument
        assert ts.timeframe is timeframe
        assert isinstance(ts.data, DataFrame)

    @pytest.mark.online
    def test_daily_data(self, datasource):
        instrument = "MSFT"
        timeframe = TimeFrame.D1
        ts = datasource.get_timeseries(
            from_date=datetime(2019, 12, 1, 9, 00, 00),
            to_date=datetime(2019, 12, 15, 23, 00, 00),
            instrument=instrument,
            timeframe=timeframe)
        assert isinstance(ts, TimeSeries)
        assert ts.instrument is instrument
        assert ts.timeframe is timeframe
        assert isinstance(ts.data, DataFrame)

    @pytest.mark.online
    def test_weekly_data(self, datasource):
        instrument = "MSFT"
        timeframe = TimeFrame.W1
        ts = datasource.get_timeseries(
            from_date=datetime(2019, 12, 1, 9, 00, 00),
            to_date=datetime(2019, 12, 15, 23, 00, 00),
            instrument=instrument,
            timeframe=timeframe)
        assert isinstance(ts, TimeSeries)
        assert ts.instrument is instrument
        assert ts.timeframe is timeframe
        assert isinstance(ts.data, DataFrame)

    @pytest.mark.online
    def test_monthly_data(self, datasource):
        instrument = "MSFT"
        timeframe = TimeFrame.MN
        ts = datasource.get_timeseries(
            from_date=datetime(2019, 12, 1, 9, 00, 00),
            to_date=datetime(2019, 12, 15, 23, 00, 00),
            instrument=instrument,
            timeframe=timeframe)
        assert isinstance(ts, TimeSeries)
        assert ts.instrument is instrument
        assert ts.timeframe is timeframe
        assert isinstance(ts.data, DataFrame)
