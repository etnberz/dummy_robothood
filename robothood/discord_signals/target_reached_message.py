from typing import Any

from robothood.discord_signals.discord_message import DiscordMessage
from robothood.discord_signals.signals import TargetReachedSignal
from robothood.discord_signals.utils import signal_regex


class TargetReachedMessage(DiscordMessage):
    """Target Reached Message Class"""

    def __eq__(self, other: Any) -> bool:
        return all([isinstance(other, TargetReachedMessage), super().__eq__(other)])

    def read_message(self) -> TargetReachedSignal:
        """Read the message and convert it into a target reached signal

        Returns
        -------
        TargetReachedSignal
            The target reached signal
        """
        signal = self.content
        quote_currency = signal_regex(pattern=r"#([^/]+)(?:/BTC|/USDT|USDT|BTC)", signal=signal)
        base_currency = str(
            signal_regex(pattern=rf"(?:#{quote_currency})([^/]+)", signal=signal)
        ).split(" ")[0]
        pair = f"{quote_currency}{base_currency}"
        target_num = str(signal_regex(pattern=r"\d+(?=st|nd|rd|th)", signal=signal))
        return TargetReachedSignal(timestamp=self.timestamp, pair=pair, target_num=target_num)
