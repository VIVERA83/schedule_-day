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
from schedule_day.schedule_day import ScheduleDay

if __name__ == "__main__":
    busy = [
        {"start": "23:30", "stop": "0:10"},
        {"start": "0:30", "stop": "1:40"},
    ]
    schedule = ScheduleDay(start_reception="23:00",
                           stop_reception="1:00",
                           time_reception="0:20",
                           busy_schedule=busy)
    print(schedule.get_free_seats())
    # output:
    # [{'start': '23:00', 'stop': '23:20'}, {'start': '00:10', 'stop': '00:30'}]
    print(schedule.add_reception(start="23:20", stop="23:40"))
    # output:
    # False
    # the reception being added intersects with the one already planned

```

### <span id="4">4. </span><span style="color:purple">Тесты</span>

Вывести результат проверки и уровень покрытия в консоль (терминал)

```bash
pytest --cov=schedule_day
```
___________________________
