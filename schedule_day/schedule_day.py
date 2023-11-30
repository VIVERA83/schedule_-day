from datetime import datetime
from typing import Literal

from .utils import seconds_to_str

Events = Literal["start", "stop"]


class EventType:
    """Event type for the Reception Scheduler.
    start: Start of reception.
    stop: End of reception.
    """

    start: Events = "start"
    stop: Events = "stop"


class ScheduleDay:
    """Reception schedule for the day."""

    def __init__(
        self,
        start_reception: str,
        stop_reception: str,
        time_reception: str,
        busy_schedule: list[dict[str, str]] = None,
    ):
        """Initialization of the schedule for the lawyer's day.

        Sets the start of the reception, and the end of the reception and the
        scheduled time for the reception.

        Args:
            start_reception: Reception start time. In the format '%H:%M'
            stop_reception: End of reception. In the format '%H:%M'
            time_reception: Planned duration of reception. In the format '%H:%M', not "0:0"
            busy_schedule: List of planned events
        """
        self._format = "%H:%M"
        self._sec_in_day = 86400
        assert (
            self.str_to_datatime(time_reception).hour
            or self.str_to_datatime(time_reception).minute
        ), "The reception time cannot be zero"
        self.start_reception = start_reception
        self.stop_reception = stop_reception
        self.time_reception = time_reception
        self.busy_schedule = busy_schedule if busy_schedule else []

    def it_inside_day(
        self,
        start_reception: str,
        stop_reception: str,
    ) -> bool:
        """Checking that the period goes beyond one day.
        if Yes then return True
        Args:
            start_reception: Reception start time. In the format '%H:%M'
            stop_reception: End of reception. In the format '%H:%M'
        """
        start = self.str_to_datatime(start_reception).timestamp()
        stop = self.str_to_datatime(stop_reception).timestamp()
        return start > stop

    def __get_busy_schedule(self) -> list[float]:
        """Converts the list of scheduled events.
        from the format 'list[dict[Events, str]]'
        to the format 'list[float]'
        needed to build a schedule with unoccupied receptions.
        """
        raw_data = []
        for interval in self.busy_schedule:
            for time_ in interval.values():
                data = self.str_to_datatime(time_).timestamp()
                if data < self.str_to_datatime(self.start_reception).timestamp():
                    data += self._sec_in_day
                raw_data.append(data)
        return raw_data

    def str_to_datatime(self, time_: str) -> datetime:
        """Converting a time string '%H:%M' to datetime."""

        data = datetime.strptime(time_, self._format)
        return data.replace(
            year=datetime.utcnow().year,
            month=datetime.utcnow().month,
            day=datetime.utcnow().day,
        )

    @staticmethod
    def datetime_to_str(data: datetime):
        """Converting a datetime to time string format '%H:%M'."""

        return data.time().isoformat()[:-3]

    def get_free_seat(self, reception_time: str = None) -> int:
        """Conversion of the planned duration of admission.

        In the format '%H:%M' in float."""
        return int(
            self.str_to_datatime(reception_time or self.time_reception).timestamp()
            - self.str_to_datatime("0:00").timestamp()
        )

    def _get_free_seats_as_list(
        self,
        start_reception: str = None,
        stop_reception: str = None,
        reception_time: str = None,
    ) -> list[list[datetime]]:
        """
        Based on the start of the reception, the end of the prem,
        the planned time for one appointment and the busy time
        for the reception, a list of free receptions is formed.

        Arg:
            start_reception: Reception start time. In the format '%H:%M'
            stop_reception: End of reception. In the format '%H:%M'
            reception_time: Planned duration of reception. In the format '%H:%M'
        """
        flag = not self.it_inside_day(
            start_reception or self.start_reception,
            stop_reception or self.stop_reception,
        )
        next_step = self.str_to_datatime(
            start_reception or self.start_reception
        ).timestamp()
        stop_time = self.str_to_datatime(
            stop_reception or self.stop_reception
        ).timestamp() + (0 if flag else self._sec_in_day)
        free_seat = self.get_free_seat(reception_time)
        busy_schedule = sorted(self.__get_busy_schedule())

        if busy_schedule:
            level = busy_schedule.pop(0)
        else:
            level = stop_time

        free_seats = []
        while next_step + free_seat <= stop_time:
            if next_step + free_seat <= level:
                free_seats.append(
                    [
                        datetime.fromtimestamp(next_step),
                        datetime.fromtimestamp(next_step + free_seat),
                    ]
                )
                next_step += free_seat
            elif busy_schedule:
                next_step = busy_schedule.pop(0)
                if busy_schedule:
                    level = busy_schedule.pop(0)
                else:
                    level = stop_time
        return free_seats

    def get_free_seats(self) -> list[dict[Events, str]]:
        """Get a list of free appointments in the schedule."""
        return [
            {
                EventType.start: self.datetime_to_str(start),
                EventType.stop: self.datetime_to_str(stop),
            }
            for start, stop in self._get_free_seats_as_list()
        ]

    def add_reception(self, start: str, stop: str) -> bool:
        """Add a new appointment to the free space in the schedule.

        If the addition is successful, it will return True

        Args:
            start: Reception start time. In the format '%H:%M'
            stop: Reception stop time. In the format '%H:%M'
        """
        if self.check_add_reception(start, stop):
            self.busy_schedule.append({EventType.start: start, EventType.stop: stop})
            return True
        return False

    def check_add_reception(self, start: str, stop: str) -> bool:
        """Checking for the possibility to add an appointment to the schedule during the specified period.

        If this period is free, True is returned True.
        Args:
            start: Reception start time. In the format '%H:%M'
            stop: Reception stop time. In the format '%H:%M'
        """

        start_reception = self.str_to_datatime(self.start_reception).timestamp()
        stop_reception = self.str_to_datatime(self.stop_reception).timestamp()
        if self.it_inside_day(self.start_reception, self.stop_reception):
            stop_reception += self._sec_in_day

        start_ = self.str_to_datatime(start).timestamp()
        stop_ = self.str_to_datatime(stop).timestamp()

        if self.it_inside_day(start, stop):
            stop_ += self._sec_in_day
        free_seat = seconds_to_str(int(stop_ - start_))

        if not self.it_inside_day(self.start_reception, self.stop_reception):
            if start_ >= start_reception and stop_ <= stop_reception:
                return bool(self._get_free_seats_as_list(start, stop, free_seat))
        if start_ < start_reception and start_ + self._sec_in_day <= stop_reception:
            return bool(self._get_free_seats_as_list(start, stop, free_seat))
        else:
            if start_ >= start_reception and stop_ <= stop_reception:
                return bool(self._get_free_seats_as_list(start, stop, free_seat))
        return False
