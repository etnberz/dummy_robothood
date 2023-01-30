from typing import Dict, Tuple

from robothood.discord_signals.signals import TradingSignal
from robothood.errors.errors import UnknownBaseAsset, UnknownPairError, WrongSignalError
from robothood.signal_managers.constants import BASE_ASSETS_INFO
from robothood.signal_managers.signal_manager import SignalManager
from robothood.signal_managers.utils import compute_buy_min_max, convert_trading_signal

# pylint:disable=unused-variable,too-many-instance-attributes


class TradingSignalManager(SignalManager):
    """Trading Signal Manager Class"""

    def __init__(self, signal: TradingSignal):
        super().__init__(signal=signal)

        if not isinstance(self.signal, TradingSignal):
            raise WrongSignalError(
                "TradingSignalManager only accepts TradingSignal as signal: your signal type "
                f"is {type(self.signal)}"
            )

        if signal.base_currency not in BASE_ASSETS_INFO:
            raise UnknownBaseAsset(
                f"Base asset {signal.base_currency} is not known or not managed by this bot yet."
            )

        symbol_info = self.client.get_symbol_info(symbol=self.signal.pair)
        if symbol_info is None:
            raise UnknownPairError(f"Pair {self.signal.pair} does not exist in Binance")

        self.market_price = float(self.client.get_ticker(symbol=self.signal.pair)["lastPrice"])
        self.signal = convert_trading_signal(message_signal=signal, market_price=self.market_price)

        self.available_base_asset_fonds = (
            float(self.client.get_asset_balance(asset=self.signal.base_currency)["free"])
            - BASE_ASSETS_INFO[self.signal.base_currency]["min_balance"]
        )

        self.oco_allowed = symbol_info["ocoAllowed"]
        lot_filters = [x for x in symbol_info["filters"] if x["filterType"] == "LOT_SIZE"][0]
        self.min_qty = float(lot_filters["minQty"])
        self.step_size = float(lot_filters["stepSize"])
        price_filters = [x for x in symbol_info["filters"] if x["filterType"] == "PRICE_FILTER"][0]
        self.tick_size = float(price_filters["tickSize"])
        self.min_buy, self.max_buy = compute_buy_min_max(
            buy_around=self.signal.buy_around,
            first_target=min(self.signal.targets),
            tick_size=self.tick_size,
        )

    # Dummy RobotHood doesn't know when the signal is ready to be processed
    def check_if_ready_to_process(self) -> bool:
        """Check if the Trading Signal is ready to be processed

        Returns
        -------
        bool
            True if ready to process
        """
        return True

    # Dummy RobotHood doesn't know how to calculate buy quantity
    def calculate_buy_quantity(self) -> float:
        """Calculate the quantity of asset to buy

        Returns
        -------
        float
            The asset quantity to buy
        """
        return 42

    # Dummy RobotHood doesn't know how to calculate sell quantities
    def calculate_sell_quantities(self) -> Dict[str, float]:
        """Calculate the quantities of asset to sell for each target.

        Returns
        -------
        float
            The asset quantities to sell
        """
        return {"T1": 42, "T2": 0, "T3": 0, "T4": 0}

    # Dummy RobotHood doesn't know how to compute selling parameters
    def compute_sell_parameters(self) -> Tuple[Dict[str, str], str, str]:
        """Compute sell parameters to fill a selling order

        Returns
        -------
        Dict[str, float]
            The asset's sell price
        str
            The asset's stop price
        str
            The asset's limit price
        """
        return {"T1": "42", "T2": "0", "T3": "0", "T4": "0"}, "42", "42"

    # Dummy RobotHood doesn't know how to process a trading message
    def process_signal(self) -> None:
        """Process the trading signal: buys and sets limit selling orders"""
        return None
