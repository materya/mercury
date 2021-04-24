#!/usr/bin/env python
# Copyright (C) 2018, 2019 - 2021 Richard Kemp
# $Id$
# -*- coding: utf-8; py-indent-offset:4 -*-

"""Python library standard setup configuration."""

import sys

from setuptools import setup
from setuptools.config import read_configuration

config = read_configuration("./setup.cfg")
name = config["metadata"]["name"]

if sys.version_info < (3, 6):
    sys.exit(f"ERROR: {name} requires Python 3.6+")

extras_packages = {
    "extra_datasource_alphavantage": [
        "alpha_vantage==2.3.1",
    ],
    "extra_datasource_quandl": [
        "quandl==3.6.1",
    ],
    "extra_datasource_polygon": [
        "polygon==0.1.9",
    ],
    "extra_broker_ig": [
        "requests",
    ],
    "extra_broker_oanda": [
        "oandapyV20==0.6.3",
    ],
}

extras = []
for value in extras_packages.values():
    extras.extend(value)


if __name__ == "__main__":
    setup(
        install_requires=[
            "numpy==1.20.1",
            "pandas==1.2.2",
            "ta-lib==0.4.19",
            "websockets",
        ],
        extras_require={
            "dev": [
                "flake8",
                "mypy",
                "pandas-stubs",
                "twine",
            ],
            "doc": [
                "pdoc3",
            ],
            "extras": extras,
            "test": [
                "flake8-annotations-coverage",
                "flake8-bandit",
                "flake8-builtins",
                "flake8-commas",
                "flake8-docstrings",
                "flake8-import-order",
                "flake8-quotes",
                "pytest",
                "pytest-cov",
                "pytest-flake8",
                "pep8-naming",
            ],
            **extras_packages,
        },
    )
