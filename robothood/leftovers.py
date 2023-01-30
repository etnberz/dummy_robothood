import logging

from robothood.hoodapi.hoodapi import get_all_opened_trading_signals
from robothood.signal_managers.trading_signal_manager import TradingSignalManager

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Running the leftovers manager")
    opened_signals = get_all_opened_trading_signals()
    if opened_signals:
        logger.info("%s opened signal found", str(len(opened_signals)))
        for signal in opened_signals:
            manager = TradingSignalManager(signal=signal)
            manager.process_signal()
    else:
        logger.info("No opened signal found")
    logger.info("End of leftovers management")
