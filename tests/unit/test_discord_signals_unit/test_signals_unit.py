import pytest

from robothood.discord_signals.signals import VALID_TARGET_NUM, TargetReachedSignal

TARGET_REACHED_ARGS = [
    (
        {
            "timestamp": "2020-11-01 13:00",
            "pair": "FRONTBTC",
            "target_num": "1",
        },
        False,
    ),
    (
        {
            "timestamp": "2020-11-01 13:00",
            "pair": "AUDIOBTC",
            "target_num": "2",
        },
        False,
    ),
    (
        {
            "timestamp": "2020-11-01 13:00",
            "pair": "LUNABTC",
            "target_num": "3",
        },
        False,
    ),
    (
        {
            "timestamp": "2020-11-01 13:00",
            "pair": "GTOBTC",
            "target_num": "4",
        },
        False,
    ),
    (
        {
            "timestamp": "2020-11-01 13:00",
            "pair": "ETHBTC",
            "target_num": "SCOOBY DOO",
        },
        True,
    ),
]


@pytest.mark.parametrize(
    "target_reached_args, error",
    TARGET_REACHED_ARGS,
    ids=[tra[0]["pair"] for tra in TARGET_REACHED_ARGS],
)
def test_target_reached_signal_init(target_reached_args, error):
    if not error:
        TargetReachedSignal(**target_reached_args)
    else:
        with pytest.raises(ValueError) as err:
            TargetReachedSignal(**target_reached_args)
        assert (
            str(err.value) == f"{target_reached_args['target_num']} is not a valid target num,"
            f" please chose among {VALID_TARGET_NUM}"
        )
