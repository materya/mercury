# Copyright (C) 2019 - 2021 Richard Kemp
# $Id$
# -*- coding: utf-8; py-indent-offset:4 -*-

"""XAPI Broker implementation Module."""

from __future__ import annotations

__copyright__ = "Copyright 2019 - 2021 Richard Kemp"
__revision__ = "$Id$"
__all__ = [
    "Broker",
]


import json
import time
from datetime import datetime, timedelta
from enum import Enum
from functools import reduce
from typing import List

from mercury import (Account, AccountType, CurrencyCode,
                     Order, OrderAction, OrderType,
                     Position, PositionStatus, PositionType, PriceType,
                     Timeframe, Timeseries)
from mercury import Broker as AbcBroker
from mercury.lib import Client
from mercury.lib.connectors import WebSocket
from mercury.lib.exceptions import NotValidPositionTypeError

import pandas as pd


class XTBTradeCommand(Enum):
    """XTB Trade transactions mapping to OrderAction."""
    BUY = 0
    SELL = 1
    BUY_LIMIT = 2
    SELL_LIMIT = 3
    BUY_STOP = 4
    SELL_STOP = 5
    BALANCE = 6
    CREDIT = 7


class XTBTradeType(Enum):
    """XTB Trade transactions type mapping to OrderType."""
    OPEN = 0
    PENDING = 1
    CLOSE = 2
    MODIFY = 3
    DELETE = 4


def reduce_candles(candles) -> pd.DataFrame:
    init_candles = {"date": [], "open": [], "high": [], "low": [],
                    "close": [], "volume": []}

    def consolidate_price(candle: dict, price: str) -> float:
        return (candle["open"] + candle[price])

    def reducer(candles, candle) -> pd.DataFrame:
        date = datetime.fromtimestamp(candle["ctm"] / 1000)
        candles["date"].append(date)
        candles["open"].append(candle["open"])
        candles["low"].append(consolidate_price(candle, "low"))
        candles["high"].append(consolidate_price(candle, "high"))
        candles["close"].append(consolidate_price(candle, "close"))
        candles["volume"].append(candle["vol"])
        return candles

    data = reduce(reducer, candles, init_candles)
    return pd.DataFrame(data).set_index("date")


WEBSOCKET_SERVER = "ws.xtb.com"


class XapiClientRequestError(Exception):
    """Raised when XAPI Client returns a functional error."""
    pass


class XapiClient(Client):
    """XAPI Client."""
    def __init__(self, websocket: WebSocket) -> None:
        self.ws = websocket

    def connect(self) -> None:
        self.ws.connect()

    def request(self, payload: dict) -> dict:
        self.__logger.debug(f"request command {payload}")
        response = self.ws.send(json.dumps(payload))

        data = json.loads(response)

        if not data["status"]:
            code = data["errorCode"]
            error = data["errorDescr"]
            self.__logger.error(f"request error {code}: {error}")
            raise XapiClientRequestError(error)
        else:
            self.__logger.debug(f"request response {data}")

        return data["streamSessionId"] if payload["command"] == "login" \
            else data["returnData"]


class Broker(AbcBroker):
    """XAPI Broker."""
    def __init__(self, *, account_id: str, login: str, password: str,
                 api_key: str, is_paper: bool = False, **kwargs) -> None:
        """Class Initializer."""
        self.is_paper = is_paper
        self.api_key = api_key
        self.login = login
        self.password = password

        super().__init__("Xapi", account_id)

    #
    # BROKER METHODS
    #

    @property
    def _client(self) -> Client:
        # Available URLs
        # wss://ws.xtb.com/demo
        # wss://ws.xtb.com/demoStream
        # wss://ws.xtb.com/real
        # wss://ws.xtb.com/realStream
        websocket_url = "wss://{server}/{endpoint}".format(
            server=WEBSOCKET_SERVER,
            endpoint="demo" if self.is_paper else "real",
        )
        ws = WebSocket(websocket_url)

        return XapiClient(ws)

    def _api_fees(self) -> float:
        return 0.0

    def _api_auth(self) -> None:
        command = {
            "command": "login",
            "arguments": {
                "userId": self.account_id,
                "password": self.password,
            },
        }
        response = self.request(command)
        print("_api_auth response", response)

    def _api_get_account(self, account_id: str = None) -> Account:
        command = {
            "command": "getMarginLevel",
        }
        data = self.request(command)

        return Account(currency=data["currency"],
                       balance=data["balance"],
                       account_type=AccountType.CASH,
                       margin=0)

    def _render_order(self, raw: dict) -> Order:
        action = OrderAction(XTBTradeCommand(raw["cmd"]).name)
        return Order(action, raw["open_price"], raw["volume"],
                     instrument=raw["symbol"], position_id=raw["position_id"],
                     id=raw["order2"],
                     raw=raw)

    def _render_position(self, raw: dict) -> Position:
        if raw["cmd"] not in [0, 1]:
            raise NotValidPositionTypeError
        direction = PositionType(XTBTradeCommand(raw["cmd"]).name)
        status = (PositionStatus.CLOSED if raw["closed"]
                  else PositionStatus.OPENED)

        return Position(direction, raw["volume"],
                        status=status,
                        id=raw["position"], reference_order_id=raw["order2"],
                        open_price=raw["open_price"],
                        open_date=raw["open_time"],
                        close_price=raw["close_price"],
                        close_date=raw["close_time"],
                        tp=raw["tp"], sl=raw["sl"], profit=raw["profit"],
                        spread=raw["spread"], taxes=raw["taxes"],
                        raw=raw)

    def _api_get_candles(self, instrument: str, timeframe: Timeframe, *,
                         start_date: datetime, end_date: datetime = None,
                         **kwargs) -> Timeseries:

        command = {
            "command": "getChartLastRequest",
            "arguments": {
                "info": {
                    "period": int(timeframe.value / 60),
                    "start": int(start_date.timestamp() * 1000),
                    "symbol": instrument,
                },
            },
        }

        data = self.request(command)
        dataframe = reduce_candles(data["rateInfos"])

        return Timeseries(instrument=instrument,
                          timeframe=timeframe,
                          dataframe=dataframe)

    def _api_get_market_price(self, instrument: str,
                              price_type: PriceType) -> float:
        # Offseting timestamp to ensure tick is available
        ts = (datetime.now() - timedelta(seconds=2)).timestamp()

        command = {
            "command": "getTickPrices",
            "arguments": {
                "level": 0,
                "symbols": [instrument],
                "timestamp": int(ts * 1000),
            },
        }

        while True:
            try:
                data = self.request(command)
                price = (data["quotations"][0]["bid"]
                         if price_type == PriceType.BID
                         else data["quotations"][0]["ask"])
                break
            except IndexError:
                time.sleep(0.1)
                pass

        self.__logger.debug(f"current market price {price} for {price_type}")

        return price

    def _api_submit_order(self, action: OrderAction, size: int, *,
                          price: float = None, currency: CurrencyCode = None,
                          instrument: str = None,
                          sl: float = None, tp: float = None) -> str:
        command = {
            "command": "tradeTransaction",
            "arguments": {
                "tradeTransInfo": {
                    "cmd": XTBTradeCommand[action.value].value,
                    "customComment": "",
                    "expiration": 0,  # expiration date - never
                    "order": 0,  # position ref for modification/deletion
                    "price": price,
                    "sl": sl,
                    "tp": tp,
                    "offset": 0,
                    "symbol": instrument,
                    "type": XTBTradeType[OrderType.OPEN.value].value,
                    "volume": size,
                },
            },
        }

        try:
            data = self.request(command)
            self.__logger.info(f"opened order {action} at {price}")
            self.__logger.debug(f"order reference {data['order']}")
        except Exception as error:
            self.__logger.error(f"failed to submit a new order: {error}")
            raise error

        return data["order"]

    def _api_get_positions(self, *args,
                           status: PositionStatus = None) -> List[Position]:
        command = {
            "command": "getTrades",
            "arguments": {
                "openedOnly": True if status == PositionStatus.OPEN else False,
            },
        }
        data = self.request(command)
        # TODO: should be in a baseclass method, not here
        positions = [self._render_position(position) for position in data] \
            if data else []

        return positions

    # def get_orders(self, *args) -> Union[List[Position], None]:
    #     command = {
    #         "command": "getTradesHistory",
    #         "arguments": {
    #             "end": 0,
    #             "start": 0,
    #         }
    #     }
    #     data = self._request(command)
    #     return data

    def _api_get_order(self, order_id: int) -> dict:
        """Temporary method => not in baseclass def.

        Should to be removed or added.
        """
        command = {
            "command": "tradeTransactionStatus",
            "arguments": {
                "order": order_id,
            },
        }
        data = self.request(command)
        return data

    def _api_close_position(self, position: Position, level: float) -> bool:
        command = {
            "command": "tradeTransaction",
            "arguments": {
                "tradeTransInfo": {
                    "expiration": 0,
                    "order": position.id,
                    "price": 1,
                    "symbol": position.instrument,
                    "type": XTBTradeType[OrderType.CLOSE.value].value,
                    "volume": 0.1,
                },
            },
        }

        data = self.request(command)
        self.__logger.info(f"closed position {position.id}")
        self.__logger.debug(f"order reference {data['order']}")

        return data

    # def get_position(self, id):
    #     path = "positions"
    #     self._client.headers.update({
    #         "Version": "2",
    #     })
    #     endpoint = "{}/{}/{}".format(self.api_url, path, id)
    #     response = self._client.get(endpoint)
    #     data = json.loads(response.content.decode("utf-8"))
    #     return data

    #
    # DATASOURCE METHODS
    #
