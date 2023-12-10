# Schedule in day

___
<span id="0"></span>

### <span id="1">1. </span><span style="color:purple">Описание</span>

Класс составляет расписание свободных `окон` приема на день отталкиваясь от следующих вводных данных:

- ```start_reception``` - начало приёма
- ```stop_reception``` - окончание приема
- ```time_reception``` - продолжительность приема, не может быть менее 1 минуты
- ```busy_schedule``` - занятые промежутки времени в которые прием не производится, необязательный параметр

### <span id="2">2. </span><span style="color:purple">Особенности</span>

1. Учтена вероятность составления графика переходящего из одного дня в другой. Пример, с 21:00 до 9:00
2. Есть метод добавления в расписание нового приема с проверкой на корректность добавления приема.
   При успешном добавлении запись, учитывается при выведении свободных приемов.

### <span id="3">3. </span><span style="color:purple">Применение</span>

```python
from schedule_day.scheduler import ScheduleDay

if __name__ == "__main__":
    busy = [
        {"start": "10:30", "stop": "10:50"},
        {"start": "18:40", "stop": "18:50"},
        {"start": "14:40", "stop": "15:50"},
        {"start": "16:40", "stop": "17:20"},
        {"start": "20:05", "stop": "20:20"},
    ]

    schedule = ScheduleDay(
        start_reception="9:00",
        stop_reception="21:00",
        time_reception="0:30",
        busy_schedule=busy,
    )
    print(*schedule.get_free_seats(), sep="\n")
    # output:
    # {'start': '09:00', 'stop': '09:30'}
    # {'start': '09:30', 'stop': '10:00'}
    # {'start': '10:00', 'stop': '10:30'}
    # {'start': '10:50', 'stop': '11:20'}
    # {'start': '11:20', 'stop': '11:50'}
    # {'start': '11:50', 'stop': '12:20'}
    # {'start': '12:20', 'stop': '12:50'}
    # {'start': '12:50', 'stop': '13:20'}
    # {'start': '13:20', 'stop': '13:50'}
    # {'start': '13:50', 'stop': '14:20'}
    # {'start': '15:50', 'stop': '16:20'}
    # {'start': '17:20', 'stop': '17:50'}
    # {'start': '17:50', 'stop': '18:20'}
    # {'start': '18:50', 'stop': '19:20'}
    # {'start': '19:20', 'stop': '19:50'}
    # {'start': '20:20', 'stop': '20:50'}
    print(schedule.add_reception(start="10:00", stop="10:30"))
    # output:
    # True
    print(*schedule.busy_schedule, sep="\n")
    # output:
    # {'start': '10:30', 'stop': '10:50'}
    # {'start': '18:40', 'stop': '18:50'}
    # {'start': '14:40', 'stop': '15:50'}
    # {'start': '16:40', 'stop': '17:20'}
    # {'start': '20:05', 'stop': '20:20'}
    # {'start': '10:00', 'stop': '10:30'} new added reception

```

### <span id="4">4. </span><span style="color:purple">Тесты</span>

Вывести результат проверки и уровень покрытия в консоль (терминал)

```bash
pytest --cov=schedule_day
```
___________________________
