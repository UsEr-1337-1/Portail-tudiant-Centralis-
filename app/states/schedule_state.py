import reflex as rx
from typing import TypedDict
import datetime


class Course(TypedDict):
    id: int
    subject: str
    professor: str
    room: str
    start_time: str
    end_time: str
    day_of_week: int
    color: str


class ScheduleState(rx.State):
    full_schedule: list[Course] = [
        {
            "id": 1,
            "subject": "Mathématiques avancées",
            "professor": "Dr. Turing",
            "room": "A101",
            "start_time": "08:00",
            "end_time": "10:00",
            "day_of_week": 0,
            "color": "#4A90E2",
        },
        {
            "id": 2,
            "subject": "Physique Quantique",
            "professor": "Dr. Feynman",
            "room": "B203",
            "start_time": "10:00",
            "end_time": "12:00",
            "day_of_week": 0,
            "color": "#D0021B",
        },
        {
            "id": 3,
            "subject": "Algorithmique",
            "professor": "Dr. Knuth",
            "room": "C305",
            "start_time": "14:00",
            "end_time": "16:00",
            "day_of_week": 1,
            "color": "#F5A623",
        },
        {
            "id": 4,
            "subject": "Anglais des affaires",
            "professor": "Mrs. Austen",
            "room": "D110",
            "start_time": "09:00",
            "end_time": "11:00",
            "day_of_week": 2,
            "color": "#7ED321",
        },
        {
            "id": 5,
            "subject": "Projet de fin d'année",
            "professor": "Dr. Hopper",
            "room": "E401",
            "start_time": "13:00",
            "end_time": "17:00",
            "day_of_week": 3,
            "color": "#BD10E0",
        },
        {
            "id": 6,
            "subject": "Base de données",
            "professor": "Dr. Codd",
            "room": "F101",
            "start_time": "10:00",
            "end_time": "12:00",
            "day_of_week": 4,
            "color": "#50E3C2",
        },
    ]
    current_date: str = datetime.date.today().isoformat()

    @rx.var
    def get_current_date(self) -> datetime.date:
        return datetime.date.fromisoformat(self.current_date)

    @rx.var
    def current_week_start(self) -> str:
        current_day = self.get_current_date
        start_of_week = current_day - datetime.timedelta(days=current_day.weekday())
        return start_of_week.strftime("%d/%m/%Y")

    @rx.event
    def previous_week(self):
        current_day = self.get_current_date
        self.current_date = (current_day - datetime.timedelta(weeks=1)).isoformat()

    @rx.event
    def next_week(self):
        current_day = self.get_current_date
        self.current_date = (current_day + datetime.timedelta(weeks=1)).isoformat()

    def _get_classes_for_day(self, day_index: int) -> list[Course]:
        return [
            course
            for course in self.full_schedule
            if course["day_of_week"] == day_index
        ]

    @rx.var
    def classes_by_day(self) -> dict[int, list[Course]]:
        classes = {i: [] for i in range(7)}
        for course in self.full_schedule:
            classes[course["day_of_week"]].append(course)
        return classes

    @rx.var
    def today_classes(self) -> list[Course]:
        today = datetime.date.today().weekday()
        return self._get_classes_for_day(today)