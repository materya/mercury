# Copyright (C) 2019 - 2021 Richard Kemp
# $Id$
# -*- coding: utf-8; py-indent-offset:4 -*-

"""Shared fixtures between unit tests."""

__copyright__ = "Copyright 2019 - 2021 Richard Kemp"
__revision__ = "$Id$"

import pandas as pd
import pytest
from numpy import array, random


@pytest.fixture
def dataset():
    return {
        "date": pd.date_range(pd.datetime.today(), periods=50, freq="H")
                  .tolist(),
        "open": array(random.uniform(low=0.83, high=0.96, size=(50,)),
                      dtype=float),
        "high": array(random.uniform(low=0.83, high=0.96, size=(50,)),
                      dtype=float),
        "low": array(random.uniform(low=0.83, high=0.96, size=(50,)),
                     dtype=float),
        "close": array(random.uniform(low=0.83, high=0.96, size=(50,)),
                       dtype=float),
        "adj_close": array(random.uniform(low=0.83, high=0.96, size=(50,)),
                           dtype=float),
        "volume": array(random.uniform(low=200, high=1500, size=(50,)),
                        dtype=int),
    }
