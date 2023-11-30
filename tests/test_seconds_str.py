import pytest

import schedule_day


@pytest.mark.parametrize(
    "seconds,result",
    [
        (0, "00:00"),
        (1, "00:00"),
        (5, "00:00"),
        (60, "00:01"),
        (75, "00:01"),
        (3700, "01:01"),
        (93600, "02:00"),
    ],
)
def test_prime(seconds, result):
    assert schedule_day.seconds_to_str(seconds) == result
