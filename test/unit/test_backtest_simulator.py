import pytest

from mercury.backtest import Simulator


# bt = Simulator(StrategySMACrossOver, 'EURUSD', datastore=, datasource=csv_ds)

# results = bt.run(from='2019-01-01', to='2020-01-01', timeframe=Timeframe.H1)
# results.print()
# results.plot()
# results.export(ExportType.PDF)

# results => Report type
# Report methods : print, plot, export(pdf, html, json, csv)
# -> report info should vary depending on a simple run or from an optimize one

class TestSimulator():
    pass

    # sanitychecks strategy inheritance
    # sanitychecks datastore inheritance
    # sanitychecks datasource inheritance
    # instrument type ?

    # RUN
    # sanitychecks range date + timeframe available in datastore, without skip
    # and ordered (see method from backtesting)
    # sanitychecks fallback to datasource if missing value in datastore (?)
    # do a test run (make a simple strategy with predictable results)
    # test a strategy error ?

    # Q: is the backtest should retrieve fresh data in datasource
    # if not available in datastore ?
    # => segregation concern ? 2 steps :
    #   - if we know data are not available in datastore
    #   - retrieve it from a datasource first and populate datastore with it
    #   - maybe datastore should be able to do it as precondition or
    #       sanity checks method before injecting it to the Simulator

    # optimize
    # same as run but how to provide array of variable parameters linked to
    # the strategy ? => need to refactor a Strategy init signature ?
    # same check as for a run => group tests
    # make a run with predictable result and determine best parameters

    # plot & results
    # how to access and return results as text and/or visualization ?
    # type of run & optimize return values ? object ?
    #   - SimulatorResults
    #   - SimulatorReport
    #   - Report

    # export as pdf ?
