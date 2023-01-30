from typing import List

VALID_TARGET_NUM = ["1", "2", "3", "4"]


class TradingSignal:  # pylint:disable=unused-variable,too-few-public-methods
    """Trading Signal Class"""

    def __init__(  # pylint:disable=too-many-arguments
        self,
        timestamp: str,
        quote_currency: str,
        base_currency: str,
        buy_around: str,
        targets: List[str],
        stop_loss: str,
    ) -> None:
        self.timestamp = timestamp
        self.quote_currency = quote_currency
        self.base_currency = base_currency
        self.pair = f"{quote_currency}{base_currency}"
        self.buy_around = float(buy_around)
        self.targets = [float(target) for target in targets]
        self.stop_loss = float(stop_loss)

    def __repr__(self) -> str:
        return (
            f"Trading Signal: Signal received at {self.timestamp}: Buy {self.pair} at around"
            f" {str(self.buy_around)} | Sell Targets "
            f"{'-'.join([str(el) for el in self.targets])}"
            f" | Stop Loss at {str(self.stop_loss)}"
        )

    def __eq__(self, other):  # type:ignore
        return all(
            [
                isinstance(other, TradingSignal),
                self.timestamp == other.timestamp,
                self.quote_currency == other.quote_currency,
                self.base_currency == other.base_currency,
                self.pair == other.pair,
                self.buy_around == other.buy_around,
                self.targets == other.targets,
                self.stop_loss == other.stop_loss,
            ]
        )


class TargetReachedSignal:  # pylint:disable=unused-variable,too-few-public-methods
    """Target Reached Signal Class"""

    def __init__(  # pylint:disable=too-many-arguments
        self,
        timestamp: str,
        pair: str,
        target_num: str,
    ) -> None:
        self.timestamp = timestamp
        self.pair = pair
        if target_num not in VALID_TARGET_NUM:
            raise ValueError(
                f"{target_num} is not a valid target num, please chose among {VALID_TARGET_NUM}"
            )
        self.target_num = target_num

    def __repr__(self) -> str:
        return (
            f"Target Reached Signal: Signal received at {self.timestamp}: Target {self.target_num}"
            f" reached for pair {self.pair}"
        )

    def __eq__(self, other):  # type:ignore
        return all(
            [
                isinstance(other, TargetReachedSignal),
                self.timestamp == other.timestamp,
                self.pair == other.pair,
                self.target_num == other.target_num,
            ]
        )
