import pytest

from schedule_day import ScheduleDay


@pytest.fixture
def schedule() -> ScheduleDay:
    """Not editable."""
    return ScheduleDay(
        start_reception="9:00", stop_reception="12:00", time_reception="0:30"
    )


@pytest.fixture
def schedule_new_day() -> ScheduleDay:
    """Not editable."""
    return ScheduleDay(
        start_reception="23:00", stop_reception="1:00", time_reception="0:30"
    )
