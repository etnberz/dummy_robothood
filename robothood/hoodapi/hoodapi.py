import logging
from typing import Any, List
from uuid import uuid4

from peewee import SqliteDatabase

from robothood.discord_signals.signals import TradingSignal
from robothood.hoodapi.peewee_models import DB_PATH, TradingSignalModel

logger = logging.getLogger(__name__)

# pylint:disable=unused-variable

VALID_STATUS = ["MISSED", "SOLD"]


def create_database() -> None:
    """Create the Database"""
    data_base = SqliteDatabase(DB_PATH)
    data_base.create_tables([TradingSignalModel])


def post_trading_signal(trading_signal: TradingSignal, status: str = "OPEN") -> Any:
    """Post trading signal on the database

    Parameters
    ----------
    trading_signal: TradingSignal
        The trading signal to post on the database
    status: str
        Status of the order placed on the signal

    Returns
    -------
    Any
        Code 1 if it worked
    """

    model = TradingSignalModel(
        timestamp=trading_signal.timestamp,
        uuid=uuid4(),
        pair=trading_signal.pair,
        quote_currency=trading_signal.quote_currency,
        base_currency=trading_signal.base_currency,
        buy_around=trading_signal.buy_around,
        target_1=trading_signal.targets[0],
        target_2=trading_signal.targets[1],
        target_3=trading_signal.targets[2],
        target_4=trading_signal.targets[3],
        stop_loss=trading_signal.stop_loss,
        status=status,
    )

    return model.save()


def get_all_opened_trading_signals() -> List[TradingSignal]:
    """Get all the opened trading signals from database as a list

    Returns
    -------
    List[TradingSignal]
        All the trading signals in the database in a list

    """
    result = []
    opened_signals = list(TradingSignalModel.select().where(TradingSignalModel.status == "OPEN"))
    for signal_model in opened_signals:
        signal = TradingSignal(
            timestamp=signal_model.timestamp,
            quote_currency=signal_model.quote_currency,
            base_currency=signal_model.base_currency,
            buy_around=signal_model.buy_around,
            targets=[
                signal_model.target_1,
                signal_model.target_2,
                signal_model.target_3,
                signal_model.target_4,
            ],
            stop_loss=signal_model.stop_loss,
        )
        # Because TradingSignal init does BTC price conversion twice:
        signal.buy_around = signal_model.buy_around
        signal.targets = [
            signal_model.target_1,
            signal_model.target_2,
            signal_model.target_3,
            signal_model.target_4,
        ]
        signal.stop_loss = signal_model.stop_loss
        result.append(signal)
    return result


def update_status_for_opened_pair(pair: str, new_status: str) -> None:
    """Update the status of the opened trading signals corresponding to the pair

    Parameters
    ----------
    pair: str
        The pair you want to get open order from
    new_status: str
        The new status of your trading signal: SOLD or MISSED

    Raises
    ------
    ValueError
        {new_status} is not a valid status, please chose a status among {VALID_STATUS}.

    """

    if new_status not in VALID_STATUS:
        raise ValueError(
            f"{new_status} is not a valid status, please chose a status among {VALID_STATUS}."
        )

    opened_signals = list(
        TradingSignalModel.select().where(
            (TradingSignalModel.status == "OPEN") & (TradingSignalModel.pair == pair)
        )
    )

    if not opened_signals:
        logger.info("No opened order for the pair %s", pair)

    else:
        for signal in opened_signals:
            signal.status = new_status
            signal.save()
            logger.info("Signal status updated to %s in the DB", new_status)
