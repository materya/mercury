# Copyright (C) 2019 - 2021 Richard Kemp
# $Id$
# -*- coding: utf-8; py-indent-offset:4 -*-

"""IG Broker implementation Module."""

from __future__ import annotations

__copyright__ = "Copyright 2019 - 2021 Richard Kemp"
__revision__ = "$Id$"
__all__ = [
    "Broker",
]


import json
from datetime import datetime
from functools import reduce
from typing import List

# from mercury import (Account, AccountType, Broker, CurrencyCode,
#                      Order, OrderAction, OrderType,
#                      Position, PositionStatus, PositionType, PriceType,
#                      Timeframe, Timeseries)
# from mercury.lib import Client, Datasource
from mercury import (Account, AccountType, CurrencyCode,
                     Order, OrderAction,
                     Position, PositionStatus, PriceType,
                     Timeframe, Timeseries)
from mercury import Broker as AbcBroker
from mercury.lib import Client

import pandas as pd

import requests


TIMEFRAME_MAP = {
    Timeframe.S: "SECOND",
    Timeframe.M1: "MINUTE",
    Timeframe.M5: "MINUTE_5",
    Timeframe.M15: "MINUTE_15",
    Timeframe.M30: "MINUTE_30",
    Timeframe.H1: "HOUR",
    Timeframe.H4: "HOUR_4",
    Timeframe.D1: "DAY",
    Timeframe.W1: "WEEK",
    Timeframe.MN: "MONTH",
}


def reduce_candles(candles) -> pd.DataFrame:
    init_candles = {"date": [], "open": [], "high": [], "low": [],
                    "close": [], "volume": []}

    def avg_price(candle: dict) -> float:
        return (candle["bid"] + candle["ask"]) / 2

    def reducer(candles, candle):
        date_format = "%Y/%m/%d %H:%M:%S"
        date = datetime.strptime(candle["snapshotTime"], date_format)
        candles["date"].append(date)
        candles["open"].append(avg_price(candle["openPrice"]))
        candles["high"].append(avg_price(candle["highPrice"]))
        candles["low"].append(avg_price(candle["lowPrice"]))
        candles["close"].append(avg_price(candle["closePrice"]))
        candles["volume"].append(candle["lastTradedVolume"])
        return candles

    data = reduce(reducer, candles, init_candles)
    return pd.DataFrame(data).set_index("date")


class IgClientRequestError(Exception):
    """Raised when Ig Client returns a functional error."""
    pass


class IgAccountNotFoundError(Exception):
    """Raised when the account_id provided does not exist on Ig platform."""
    pass


class IgClient(Client):
    """Ig Client."""
    def __init__(self, url: str, api_key: str) -> None:
        session = requests.Session()
        session.headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "application/json; charset=UTF-8",
            "VERSION": "2",
            "X-Ig-API-KEY": api_key,
        }
        self.url = url
        self.session = session

    def connect(self) -> None:
        pass

    def request(self, payload: dict, *,
                method: str, endpoint: str, version: int = 2) -> dict:
        self.__logger.debug(f"request to {endpoint} with command {payload}")
        url = "{}/{}".format(self.url, endpoint)

        headers = {"VERSION": str(version)}
        if method == "get":
            response = self.session.request(method, url, headers=headers)
        else:
            response = self.session.request(method, url, json=payload,
                                            headers=headers)

        # TODO: Add response content validation + errors
        if (method == "post" and endpoint == "session"):
            self.session.headers.update({
                "X-SECURITY-TOKEN": response.headers["X-SECURITY-TOKEN"],
                "CST": response.headers["CST"],
            })

        print("RESPONSE REQUEST", response.request.headers)
        print("RESPONSE REQUEST", response.request.body)
        print("RESPONSE", response.text)
        data = json.loads(response.content.decode("utf-8"))
        return data


class Broker(AbcBroker):
    """Ig Broker."""
    def __init__(self, *, account_id: str, login: str, password: str,
                 api_key: str, is_paper: bool = False, **kwargs) -> None:
        """Class Initializer."""
        self.is_paper = is_paper
        self._api_key = api_key
        self._login = login
        self._password = password
        self._oauth = {}

        super().__init__("Ig", account_id)

    #
    # BROKER METHODS
    #

    @property
    def _client(self) -> Client:
        server = "demo-api.ig.com" if self.is_paper else "api.ig.com"
        url = f"https://{server}/gateway/deal"

        return IgClient(url, self._api_key)

    def _api_fees(self) -> float:
        return 0.0

    def _api_auth(self) -> None:
        payload = {
            "identifier": self._login,
            "password": self._password,
        }
        response = self.request(payload, method="post", endpoint="session")
        print("_api_auth response", response)

    def _api_get_account(self, account_id: str = None) -> Account:
        response = self.request({}, method="get", endpoint="accounts",
                                version=1)
        # TODO: handle not found account
        try:
            account = next(account for account in response["accounts"]
                           if account["accountId"] == account_id)
        except StopIteration:
            # self.__logger.error(f"unable to find account {account_id}")
            raise IgAccountNotFoundError(f"account {account_id} not found") \
                from None
        return Account(currency=account["currency"],
                       balance=account["balance"]["available"],
                       account_type=AccountType.CASH,
                       margin=0)

    def _render_order(self, raw: dict) -> Order:
        pass

    def _render_position(self, raw: dict) -> Position:
        pass

    def _api_get_candles(self, instrument: str, timeframe: Timeframe, *,
                         start_date: datetime, end_date: datetime = None,
                         **kwargs) -> Timeseries:
        path = "prices/{}/{}/{}/{}".format(
            instrument,
            TIMEFRAME_MAP[timeframe],
            start_date,
            end_date,
        )
        response = self.request({}, method="get", endpoint=path)

        dataframe = reduce_candles(response["prices"])

        return Timeseries(instrument=instrument,
                          timeframe=timeframe,
                          dataframe=dataframe)

    def _api_get_positions(self, *args,
                           status: PositionStatus = None) -> List(Position):
        response = self.request({}, method="get", endpoint="positions")

        def format_position(position):
            values = position["position"]
            return Position(values["size"], values["createdDateUTC"],
                            broker=self, id=values["dealId"],
                            sl=values["stopLevel"], tp=values["limitLevel"])
        positions = [format_position(p) for p in response["positions"]]

        return positions

    def _api_submit_order(self, action: OrderAction, size: int, *,
                          price: float = None, currency: CurrencyCode = None,
                          instrument: str = None,
                          sl: float = None, tp: float = None) -> str:
        endpoint = "{}/{}".format(self.api_url, "positions/otc")
        payload = {
            "currencyCode": currency,
            # "direction": direction.value,
            "epic": instrument,
            "expiry": "-",
            "orderType": type.value,
            "size": size,
            "limitLevel": tp,
            "stopLevel": sl,
            "forceOpen": True,
            "guaranteedStop": False,
        }
        print("open position", payload)
        self._client.headers.update({
            "Version": "2",
        })
        response = self._client.post(endpoint, json=payload)
        print("opening position: ", response.content.decode("utf-8"))
        # TODO: handle not found account
        data = json.loads(response.content.decode("utf-8"))
        if response.status_code == 200:
            position = Position(size, datetime.now(), raw=payload,
                                broker=self, id=data["dealReference"],
                                sl=sl, tp=tp)
            self._positions.append(position)
        else:
            print("error opening position", data)

    # TODO: refactor
    # def _api_close_position(self, position: Position,
    #                         instrument: str) -> bool:
    #     direction = (TradeType.SELL
    #                  if position._direction == TradeType.BUY
    #                  else TradeType.BUY)
    #     order_type = OrderType.MARKET
    #     endpoint = "{}/{}".format(self.api_url, "positions/otc")
    #     self._client.headers.update({
    #         "Version": "1",
    #         "_method": "DELETE",
    #     })
    #     payload = {
    #         "dealId": position._id,
    #         "orderType": order_type.value,
    #         "size": str(position._size),
    #         "direction": direction.value,
    #     }
    #     response = self._client.post(endpoint, json=payload)
    #     # print("body", response.request.body)
    #     # print("response", response.content.decode("utf-8"))
    #     data = json.loads(response.content.decode("utf-8"))
    #     del self._client.headers["_method"]
    #     if response.status_code == 200:
    #         self._positions.remove(position)
    #         return True
    #     else:
    #         print("error closing position", data)
    #         return False

    # def get_position(self, id):
    #     path = "positions"
    #     self._client.headers.update({
    #         "Version": "2",
    #     })
    #     endpoint = "{}/{}/{}".format(self.api_url, path, id)
    #     response = self._client.get(endpoint)
    #     data = json.loads(response.content.decode("utf-8"))
    #     return data

    def _api_get_market_price(self, instrument: str,
                              price_type: PriceType) -> float:
        path = "markets/{}".format(instrument)
        response = self.request({}, method="get", endpoint=path, version=3)
        return (response["snapshot"]["bid"] if price_type == PriceType.BID
                else response["snapshot"]["offer"])

    def _api_close_position():
        pass
