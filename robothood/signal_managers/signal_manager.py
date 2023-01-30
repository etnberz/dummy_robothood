import os
from abc import ABC
from typing import Any

from binance import Client

# pylint:disable=too-few-public-methods,unused-variable


class SignalManager(ABC):
    """Signal Manager Class"""

    def __init__(self, signal: Any):
        self.signal = signal
        self.client = Client(api_key=os.environ["BAPI_KEY"], api_secret=os.environ["BAPI_SECRET"])
