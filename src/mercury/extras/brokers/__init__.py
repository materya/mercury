# Copyright (C) 2019 - 2021 Richard Kemp
# $Id$
# -*- coding: utf-8; py-indent-offset:4 -*-

"""Mercury Brokers Extras Module."""

__copyright__ = "Copyright 2019 - 2021 Richard Kemp"
__revision__ = "$Id$"
__all__ = [
    "IG",
    "Oanda",
    "XAPI",
]

from .ig import IG
from .oanda import Oanda
from .xapi import XAPI
