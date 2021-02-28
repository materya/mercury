# Copyright (C) 2019 - 2021 Richard Kemp
# $Id$
# -*- coding: utf-8; py-indent-offset:4 -*-

"""Mercury Account module.

TODO: docs goes here
"""


from __future__ import annotations


__copyright__ = "Copyright 2019 - 2021 Richard Kemp"
__revision__ = "$Id$"
__all__ = [
    "Account",
    "AccountType",
]


from enum import Enum

from ..lib import BaseClass


class AccountType(Enum):
    """Different type of accounts."""
    CASH = "CASH"
    MARGIN = "MARGIN"


class Account(BaseClass):
    """Internal representation of a broker's account.

    Attributes:
        currency (str): Account's base currency.
        balance (float): Account's current balance.
        capital (float): Account's initial balance (before live trading
            or backtest).
        type (AccountType): CASH or MARGIN account.
        margin (float): Account's allowed margin from the broker.
        raw_data (dict): Broker's raw account representation (just in case).

    Usage::
        >>> from mercury import Account
        >>> account = Account(currency="EUR", balance="12345")
    """
    # TODO: where to put lotsize ? Account, Stragegy, else ?
    def __init__(self, *, currency: str, balance: float,
                 account_type: AccountType = AccountType.CASH,
                 margin: float = None, raw_data: dict = {}) -> None:
        """Class initializer.

        Args:
            currency: Account's currency.
            balance: Account's initial balance.
            account_type: CASH or MARGIN account.
            margin: Account's allowed margin from the broker.
            raw_data: Broker's raw account representation data.
        """
        self.currency = currency
        self.capital = balance
        self.balance = balance
        self.type = account_type
        self.margin = margin
        self.raw_data = raw_data

    def __repr__(self) -> str:
        """Override of __repr__."""
        # TODO: test if margin or cash to adapt string visual
        return ("<Account: ({currency}){balance} {type}({margin})>"
                .format(currency=self.currency,
                        balance=self.balance,
                        type=self.type.name,
                        margin=self.margin))

    __str__ = __repr__
