# -*- coding: utf-8 -*-

import openai
from icalendar import Event, Calendar
from datetime import datetime, timedelta

# Замените YOUR_API_KEY на ваш API-ключ от OpenAI
openai.api_key = "YOUR_API_KEY"


def generate_schedule(raw_schedule):
    prompt = f"Построй для меня в ответном на это сообщение идеальный распорядок идеального дня на завтра. Заполни мне график на весь день. Учитывай мои планы на день, которые я напишу внизу этого сообщения.\nРаспорядок дня должен быть в следующем формате:\nВремя начала до Время окончания - Название события\nКаждое событие начинается с новой строки.\nНапример, расписание может выглядеть так:\n08:00 до 09:00 - Подъем\n09:00 до 10:00 - Завтрак\n10:00 до 11:00 - Работа\nКаждое событие должно быть указано на новой строке с временем начала, указанным в формате 24-часового времени (например, 13:00), за которым следует тире и название события. Ответное сообщение должно содержать только расписание и больше ничего.\nМои планы:\n{raw_schedule}"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=400,
        n=1,
        stop=None,
        temperature=0.7,
    )

    schedule = response.choices[0].text.strip()
    return schedule


def create_ical_file(schedule, filename="my_schedule.ics"):
    cal = Calendar()
    cal.add("prodid", "-//My Schedule//example.com//")
    cal.add("version", "2.0")

    for line in schedule.split("\n"):
        start_time, end_time, summary = line.split(" - ")[0].split(" до ")[0], line.split(" - ")[0].split(" до ")[1], \
        line.split(" - ")[1]
        event_start = datetime.strptime(start_time, "%H:%M") + timedelta(days=1)
        event_end = datetime.strptime(end_time, "%H:%M") + timedelta(days=1)

        event = Event()
        event.add("summary", summary)
        event.add("dtstart", event_start)
        event.add("dtend", event_end)
        event.add("dtstamp", datetime.now())
        cal.add_component(event)

    with open(filename, "wb") as f:
        f.write(cal.to_ical())


def main():
    raw_schedule = input("Введите ваше расписание на завтра в свободной форме: ")
    schedule = generate_schedule(raw_schedule)
    print("Ваше идеальное расписание на завтра:")
    print(schedule)
    create_ical_file(schedule)
    print("Расписание сохранено в файл my_schedule.ics")


if __name__ == "__main__":
    main()
