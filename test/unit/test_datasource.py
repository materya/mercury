import pytest

import numpy as np
from pandas import DataFrame

from mercury.lib import Datasource


class TestDatasource():
    def test_direct_invocation(self):
        with pytest.raises(TypeError):
            source = Datasource()
