from typing import Any

from robothood.discord_signals.constants import PAIR_KEYWORDS, REGEX_PATTERNS
from robothood.discord_signals.discord_message import DiscordMessage
from robothood.discord_signals.signals import TradingSignal
from robothood.discord_signals.utils import pick_line, signal_regex


class TradingMessage(DiscordMessage):
    """Trading Message Class"""

    def __eq__(self, other: Any) -> bool:
        return all([isinstance(other, TradingMessage), super().__eq__(other)])

    def read_message(self) -> TradingSignal:
        """Read the message and convert it into a trading signal

        Returns
        -------
        TradingSignal
            The trading signal
        """
        signal = self.content
        signal_list = [el for el in signal.split("\n") if el != ""]

        trading_signal_dict = {"timestamp": self.timestamp}

        for k in REGEX_PATTERNS:
            trading_signal_dict[k] = signal_regex(
                pattern=REGEX_PATTERNS[k]["pattern"],  # type: ignore
                signal=pick_line(
                    signal_list=signal_list, keywords=REGEX_PATTERNS[k]["keywords"]  # type: ignore
                ),
            )
        trading_signal_dict["base_currency"] = signal_regex(
            pattern=rf'(?:PAIR: {trading_signal_dict["quote_currency"]}/)([^/]+)',
            signal=pick_line(signal_list=signal_list, keywords=PAIR_KEYWORDS),  # type: ignore
        ).split(" ")[0]
        return TradingSignal(**trading_signal_dict)
