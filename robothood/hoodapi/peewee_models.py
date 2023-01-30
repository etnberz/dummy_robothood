import os
from pathlib import Path

from peewee import CharField, DateTimeField, FloatField, Model, SqliteDatabase

DB_PATH = Path(os.environ["ROBOTHOOD_PATH"]) / "database/robothood.db"

data_base = SqliteDatabase(DB_PATH)


# pylint:disable=too-few-public-methods,unused-variable


class TradingSignalModel(Model):  # type:ignore
    """Trading Signal Peewee Model Class"""

    timestamp = DateTimeField()
    uuid = CharField()
    quote_currency = CharField()
    base_currency = CharField()
    pair = CharField()
    buy_around = FloatField()
    target_1 = FloatField()
    target_2 = FloatField()
    target_3 = FloatField()
    target_4 = FloatField()
    stop_loss = FloatField()
    status = CharField()

    class Meta:
        """Meta Class from Peewee Model"""

        database = data_base
        table_name = "trading_signal"
