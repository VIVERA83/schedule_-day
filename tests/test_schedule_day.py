import pytest

from tests.utils import *


class TestScheduleDay:
    @pytest.mark.parametrize(
        "time_,result",
        [
            ("9:0", datetime(*git_date_now(), hour=9, minute=0)),
            ("00:00", datetime(*git_date_now(), hour=0, minute=0)),
            ("0:1", datetime(*git_date_now(), hour=0, minute=1)),
            ("2:11", datetime(*git_date_now(), hour=2, minute=11)),
            ("23:59", datetime(*git_date_now(), hour=23, minute=59)),
        ],
    )
    def test_str_to_datatime(self, schedule, time_, result):
        assert result == schedule.str_to_datatime(time_)

    @pytest.mark.parametrize(
        "result,time_",
        [
            ("09:00", datetime(*git_date_now(), hour=9, minute=0)),
            ("00:00", datetime(*git_date_now(), hour=0, minute=0)),
            ("00:01", datetime(*git_date_now(), hour=0, minute=1)),
            ("02:11", datetime(*git_date_now(), hour=2, minute=11)),
            ("23:59", datetime(*git_date_now(), hour=23, minute=59)),
        ],
    )
    def test_datetime_to_str(self, schedule, time_, result):
        assert result == schedule.datetime_to_str(time_)

    @pytest.mark.parametrize(
        "time_,result ",
        [
            ("0:10", 600),
            ("01:10", 4200),
            ("23:59", 86340),
            # schedule_short_free.reception_time = "00:30"
            (None, 1800),
        ],
    )
    def test_get_free_seat(self, schedule, time_, result):
        assert result == schedule.get_free_seat(time_)

    @pytest.mark.parametrize(
        "reception_time,busy,result ",
        [
            ("0:30", [], free_seats_1),
            ("1:30", [], free_seats_2),
            ("2:01", [], free_seats_3),
            ("4:30", [], free_seats_4),
            ("0:45", busy_5, free_seats_5),
            ("0:30", busy_6, free_seats_6),
        ],
    )
    def test_get_free_seats(self, schedule, reception_time, busy, result):
        schedule.time_reception = reception_time
        schedule.busy_schedule = busy
        assert result == schedule.get_free_seats()

    @pytest.mark.parametrize(
        "reception_time,busy,result ",
        [
            ("0:30", busy_9, free_seats_9),
            ("1:30", [], free_seats_10),
            ("0:17", busy_11, free_seats_11),
        ],
    )
    def test_get_free_seats_new_day(
        self, schedule_new_day, reception_time, busy, result
    ):
        schedule_new_day.time_reception = reception_time
        schedule_new_day.busy_schedule = busy
        assert result == schedule_new_day.get_free_seats()

    @pytest.mark.parametrize(
        "start,stop,busy,result ",
        [
            ("23:50", "0:05", [], True),
            ("23:50", "0:05", busy_11, False),
            ("22:00", "12:01", busy_11, False),
            ("00:10", "00:20", [], True),
            # ("9:45", "10:15", busy_6, False),
            # ("10:15", "10:30", busy_6, True),
        ],
    )
    def test_check_add_reception_2(self, schedule_new_day, start, stop, busy, result):
        schedule_new_day.busy_schedule = busy
        assert result == schedule_new_day.check_add_reception(start, stop)

    @pytest.mark.parametrize(
        "start,stop,busy,result ",
        [
            ("8:30", "9:30", [], False),
            ("9:00", "9:30", [], True),
            ("12:00", "12:01", [], False),
            ("9:00", "12:00", busy_6, False),
            ("9:45", "10:15", busy_6, False),
            ("10:15", "10:30", busy_6, True),
        ],
    )
    def test_check_add_reception(self, schedule, start, stop, busy, result):
        schedule.busy_schedule = busy
        assert result == schedule.check_add_reception(start, stop)

    @pytest.mark.parametrize(
        "start,stop,busy,result,busy_result",
        [
            ("8:30", "9:30", [], False, []),
            ("9:00", "9:30", [], True, busy_7),
            ("12:00", "12:01", [], False, []),
            ("9:00", "12:00", busy_6, False, busy_6),
            ("9:45", "10:15", busy_6, False, busy_6),
            ("10:15", "10:30", busy_6, True, busy_8),
        ],
    )
    def test_add_reception(self, schedule, start, stop, busy, result, busy_result):
        schedule.busy_schedule = busy
        assert result == schedule.add_reception(start, stop)
        assert busy_result == schedule.busy_schedule
