import logging


def pytest_configure(config):
    # Too many warnings, see
    # - https://github.com/tholo/pytest-flake8/issues/42
    # - https://github.com/tholo/pytest-flake8/issues/69
    logging.getLogger('flake8').setLevel(logging.ERROR)
