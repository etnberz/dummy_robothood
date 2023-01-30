from robothood.discord_signals.signals import TargetReachedSignal
from robothood.hoodapi.hoodapi import update_status_for_opened_pair
from robothood.signal_managers.signal_manager import SignalManager

# pylint:disable=too-few-public-methods,unused-variable


class TargetReachedSignalManager(SignalManager):
    """Trading Signal Manager Class"""

    def __init__(self, signal: TargetReachedSignal):
        super().__init__(signal=signal)

    def process_signal(self) -> None:
        """Process the target reached signal: update order status"""
        update_status_for_opened_pair(pair=self.signal.pair, new_status="MISSED")
