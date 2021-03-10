import pytest

from mercury.lib import Datastore


class TestDatastore():
    pass

    # no direct invocation
    # should successfully connect to a store during init
    # raise error if connect failed

    # can store data from a panda dataframe
    # raise error if data not a panda dataframe

    # can append data to an existing store
    # raise error if name store does not exist
    # raise error if dataframe not a pandas dataframe

    # can get a name store
    # get data should be returned as a pandas dataframe
