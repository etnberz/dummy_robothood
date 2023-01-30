import pytest

from robothood.signal_managers.target_reached_signal_manager import TargetReachedSignalManager
from tests.conftest import TARGET_REACHED_SIGNALS, TestClient  # pylint:disable=import-error


@pytest.mark.parametrize(
    "target_reached_signal",
    [TARGET_REACHED_SIGNALS[pair] for pair in TARGET_REACHED_SIGNALS],
    ids=TARGET_REACHED_SIGNALS.keys(),
)
def test_process_signal(mocker, target_reached_signal):

    mocker.patch(
        "robothood.signal_managers.signal_manager.Client",
        return_value=TestClient(),
    )

    mock_update_pair_opened_trading_signals = mocker.patch(
        "robothood.signal_managers.target_reached_signal_manager.update_status_for_opened_pair",
    )

    manager = TargetReachedSignalManager(signal=target_reached_signal)
    manager.process_signal()

    mock_update_pair_opened_trading_signals.assert_called_once_with(
        pair=target_reached_signal.pair, new_status="MISSED"
    )
