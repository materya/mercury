# Copyright (C) 2019 - 2021 Richard Kemp
# $Id$
# -*- coding: utf-8; py-indent-offset:4 -*-

"""Mercury connectors module.

Define and provides several standard connectors for the Client to be able to
access APIs on different protocols such as websockets, sockets, REST, etc.
"""

from __future__ import annotations


__copyright__ = "Copyright 2019 - 2021 Richard Kemp"
__revision__ = "$Id$"
__all__ = [
    "WebSocket",
]


import asyncio
from abc import ABCMeta, abstractmethod
from typing import TypeVar

import websockets

from .baseclass import BaseClass
from .exceptions import ConnectionLostError


T = TypeVar("T")


class ConnectorMeta(ABCMeta, type(BaseClass)):
    """Connector metaclass wrapper.

    This trick is needed when you want to use more than one metaclass
    for a given class.
    """
    pass


class Connector(metaclass=ConnectorMeta):
    """Connector abstract interface class.

    This is a superclass and it should not be call directly,
    superclass it instead.
    """
    @abstractmethod
    def connect(self) -> None:
        """Should implement the behavior to connect to the remote server."""

    @abstractmethod
    def send(self, payload: T) -> T:
        """Should implement how to send a payload to the remote server."""


class WebSocket(Connector):
    """Websocket Connector.

    Implement a websocket and abstract how to send and receive data.
    """
    def __init__(self, url: str) -> None:
        """Websocket initialization."""
        self.ws = None
        self.url = url
        self.loop = asyncio.get_event_loop()

    def connect(self) -> None:
        """Start a websocket connection synchronously."""
        return self.loop.run_until_complete(self.__async__connect())

    async def __async__connect(self) -> None:
        """Async websocket connection."""
        # perform async connect
        # & store the connected WebSocketClientProtocol object for later reuse
        try:
            self.ws = await websockets.connect(self.url)
            self.__logger.info(f"connected to {self.url}")
        except Exception as error:
            self.__logger.error(f"unable to connect to {self.url}: {error}")
            raise error

    def send(self, payload: str) -> str:
        """Transmit a payload to the remote server."""
        return self.loop.run_until_complete(self.__async__send(payload))

    async def __async__send(self, payload: str) -> str:
        """Async transmission of payload data."""
        try:
            await self.ws.send(payload)
            return await self.ws.recv()
        except websockets.exceptions.ConnectionClosedError:
            self.__logger.error("connection lost")
            raise ConnectionLostError
        except Exception as error:
            self.__logger.error(f"send/recv error: ({error.__name__}) {error}")
            raise error
