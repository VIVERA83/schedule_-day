from datetime import datetime


def git_date_now() -> list[int]:
    return [datetime.utcnow().year, datetime.utcnow().month, datetime.utcnow().day]


free_seats_1 = [
    {"start": "09:00", "stop": "09:30"},
    {"start": "09:30", "stop": "10:00"},
    {"start": "10:00", "stop": "10:30"},
    {"start": "10:30", "stop": "11:00"},
    {"start": "11:00", "stop": "11:30"},
    {"start": "11:30", "stop": "12:00"},
]

free_seats_2 = [
    {"start": "09:00", "stop": "10:30"},
    {"start": "10:30", "stop": "12:00"},
]
free_seats_3 = [{"start": "09:00", "stop": "11:01"}]
free_seats_4 = []

busy_5 = [
    {"start": "10:30", "stop": "10:50"},
]
free_seats_5 = [
    {"start": "09:00", "stop": "09:45"},
    {"start": "09:45", "stop": "10:30"},
    {"start": "10:50", "stop": "11:35"},
]

busy_6 = [
    {"start": "10:30", "stop": "10:50"},
    {"start": "9:45", "stop": "10:15"},
]

free_seats_6 = [
    {"start": "09:00", "stop": "09:30"},
    {"start": "10:50", "stop": "11:20"},
    {"start": "11:20", "stop": "11:50"},
]
busy_7 = [{"start": "9:00", "stop": "9:30"}]

busy_8 = [
    {"start": "10:30", "stop": "10:50"},
    {"start": "9:45", "stop": "10:15"},
    {"start": "10:15", "stop": "10:30"},
]
busy_9 = [{"start": "23:30", "stop": "0:30"}]

free_seats_9 = [
    {"start": "23:00", "stop": "23:30"},
    {"start": "00:30", "stop": "01:00"},
]
free_seats_10 = [{"start": "23:00", "stop": "00:30"}]

busy_11 = [
    {"start": "23:30", "stop": "0:10"},
    {"start": "0:30", "stop": "0:40"},
]
free_seats_11 = [
    {"start": "23:00", "stop": "23:17"},
    {"start": "00:10", "stop": "00:27"},
    {"start": "00:40", "stop": "00:57"},
]
