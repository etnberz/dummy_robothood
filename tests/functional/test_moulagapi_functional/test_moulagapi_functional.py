from functools import wraps
from typing import List, Optional

import pytest
from playhouse.sqlite_ext import SqliteExtDatabase

from robothood.discord_signals.signals import TradingSignal
from robothood.hoodapi.hoodapi import (
    VALID_STATUS,
    get_all_opened_trading_signals,
    post_trading_signal,
    update_status_for_opened_pair,
)
from robothood.hoodapi.peewee_models import TradingSignalModel


def with_test_db(dbs: tuple, post: Optional[List[TradingSignal]] = None):
    def decorator(func):
        @wraps(func)
        def test_db_closure(*args, **kwargs):
            test_db = SqliteExtDatabase(":memory:")
            with test_db.bind_ctx(dbs):
                test_db.create_tables(dbs)
                if post is not None:
                    for ts in post.keys():
                        post_trading_signal(
                            trading_signal=post[ts]["signal"], status=post[ts]["status"]
                        )
                try:
                    func(*args, **kwargs)
                finally:
                    test_db.drop_tables(dbs)
                    test_db.close()

        return test_db_closure

    return decorator


INIT_DB = {
    "FRONTBTC": {
        "signal": TradingSignal(
            timestamp="2020-11-01 13:00",
            quote_currency="FRONT",
            base_currency="BTC",
            buy_around="1340",
            targets=["1375", "1435", "1550", "1700"],
            stop_loss="980",
        ),
        "status": "OPEN",
    },
    "AUDIOBTC": {
        "signal": TradingSignal(
            timestamp="2020-11-01 13:00",
            quote_currency="AUDIO",
            base_currency="BTC",
            buy_around="1340",
            targets=["1375", "1435", "1550", "1700"],
            stop_loss="980",
        ),
        "status": "BOUGHT",
    },
    "LUNABTC": {
        "signal": TradingSignal(
            timestamp="2020-11-01 13:00",
            quote_currency="LUNA",
            base_currency="BTC",
            buy_around="12100",
            targets=["12600", "12990", "13700", "15800"],
            stop_loss="8500",
        ),
        "status": "SELLED",
    },
    "LTCUSDT": {
        "signal": TradingSignal(
            timestamp="2020-11-01 13:00",
            quote_currency="LTC",
            base_currency="USDT",
            buy_around="61.26",
            targets=["61.90", "65.00", "69.00", "72.00"],
            stop_loss="40.00",
        ),
        "status": "OPEN",
    },
    "ALGOUSDT": {
        "signal": TradingSignal(
            timestamp="2020-11-01 13:00",
            quote_currency="ALGO",
            base_currency="USDT",
            buy_around="0.2903",
            targets=["0.2932", "0.2990", "0.3120", "0.3200"],
            stop_loss="0.2000",
        ),
        "status": "MISSED",
    },
}


@with_test_db(dbs=(TradingSignalModel,), post=None)
@pytest.mark.parametrize("to_post", [INIT_DB[ts] for ts in INIT_DB], ids=INIT_DB.keys())
def test_post_trading_signal(to_post):
    code = post_trading_signal(trading_signal=to_post["signal"], status=to_post["status"])
    assert code == 1


@with_test_db(dbs=(TradingSignalModel,), post=INIT_DB)
def test_get_all_opened_trading_signal():
    trading_signals = get_all_opened_trading_signals()
    assert trading_signals == [
        INIT_DB[ts]["signal"] for ts in INIT_DB if INIT_DB[ts]["status"] == "OPEN"
    ]


@with_test_db(dbs=(TradingSignalModel,), post=INIT_DB)
@pytest.mark.parametrize(
    "pair, new_status",
    [
        ("FRONTBTC", "MISSED"),
        ("LTCUSDT", "MISSED"),
        ("FRONTBTC", "SOLD"),
        ("LTCUSDT", "SOLD"),
        ("FRONTBTC", "SCOOBY"),
        ("LTCUSDT", "DOO"),
    ],
    ids=[
        "FRONTBTC MISSED",
        "LTCUSDT MISSED",
        "FRONTBTC SOLD",
        "LTCUSDT SOLD",
        "FRONTBTC SCOOBY",
        "LTCUSDT DOO",
    ],
)
def test_update_pair_opened_trading_signal(pair, new_status):
    original_signal = list(TradingSignalModel.select().where(TradingSignalModel.pair == pair))
    assert original_signal[0].status == "OPEN"

    if new_status not in VALID_STATUS:
        with pytest.raises(ValueError) as error:
            update_status_for_opened_pair(pair=pair, new_status=new_status)
        assert (
            str(error.value)
            == f"{new_status} is not a valid status, please chose a status among {VALID_STATUS}."
        )

    else:
        update_status_for_opened_pair(pair=pair, new_status=new_status)

        updated_signal = list(TradingSignalModel.select().where(TradingSignalModel.pair == pair))
        assert updated_signal[0].status == new_status
