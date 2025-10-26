import reflex as rx
from typing import TypedDict, Literal
import asyncio
import logging


class StudentGrade(TypedDict):
    subject: str
    grade: float
    coefficient: int
    date: str
    semester: str


class Student(TypedDict):
    id: int
    name: str
    email: str
    grades: list[StudentGrade]


class ProfessorState(rx.State):
    students_grades: list[Student] = [
        {
            "id": 1,
            "name": "Jean Dupont",
            "email": "jean.dupont@univ.fr",
            "grades": [
                {
                    "subject": "Mathématiques",
                    "grade": 16.5,
                    "coefficient": 4,
                    "date": "2024-01-15",
                    "semester": "Semestre 1",
                },
                {
                    "subject": "Physique",
                    "grade": 14.0,
                    "coefficient": 3,
                    "date": "2024-01-20",
                    "semester": "Semestre 1",
                },
            ],
        },
        {
            "id": 2,
            "name": "Marie Martin",
            "email": "marie.martin@univ.fr",
            "grades": [
                {
                    "subject": "Mathématiques",
                    "grade": 18.0,
                    "coefficient": 4,
                    "date": "2024-01-15",
                    "semester": "Semestre 1",
                },
                {
                    "subject": "Physique",
                    "grade": 15.5,
                    "coefficient": 3,
                    "date": "2024-01-20",
                    "semester": "Semestre 1",
                },
            ],
        },
        {
            "id": 3,
            "name": "Pierre Durand",
            "email": "pierre.durand@univ.fr",
            "grades": [
                {
                    "subject": "Mathématiques",
                    "grade": 12.5,
                    "coefficient": 4,
                    "date": "2024-01-15",
                    "semester": "Semestre 1",
                },
                {
                    "subject": "Physique",
                    "grade": 13.0,
                    "coefficient": 3,
                    "date": "2024-01-20",
                    "semester": "Semestre 1",
                },
            ],
        },
    ]
    selected_student_id: int = 0
    edit_mode: bool = False
    is_updating: bool = False
    selected_subject: str = ""
    new_grade_value: str = ""

    @rx.var
    def selected_student(self) -> Student | None:
        for student in self.students_grades:
            if student["id"] == self.selected_student_id:
                return student
        return None

    @rx.var
    def subjects_taught(self) -> list[str]:
        return ["Mathématiques", "Physique", "Informatique", "Algorithmique"]

    @rx.event
    def select_student(self, student_id: int):
        self.selected_student_id = student_id
        self.edit_mode = False

    @rx.event
    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode

    from app.states.notifications_state import NotificationsState

    @rx.event
    async def update_grade(self, form_data: dict):
        self.is_updating = True
        yield
        await asyncio.sleep(1)
        try:
            student_id = int(form_data["student_id"])
            subject = form_data["subject"]
            new_grade = float(form_data["new_grade"])
            for student in self.students_grades:
                if student["id"] == student_id:
                    for grade in student["grades"]:
                        if grade["subject"] == subject:
                            grade["grade"] = new_grade
                            break
                    break
            self.edit_mode = False
            self.is_updating = False
            yield rx.toast("Note mise à jour avec succès!")
            yield self.NotificationsState.add_notification(
                type="grade_update",
                content=f"Note modifiée en {subject}: {new_grade}/20",
                link="/notes",
            )
        except Exception as e:
            self.is_updating = False
            logging.exception(f"Error updating grade: {e}")
            yield rx.toast(
                "Erreur lors de la mise à jour",
                style={"background": "#F87171", "color": "white"},
            )

    @rx.event
    async def add_new_grade(self, form_data: dict):
        self.is_updating = True
        yield
        await asyncio.sleep(1)
        try:
            student_id = int(form_data["student_id"])
            subject = form_data["subject"]
            grade = float(form_data["grade"])
            coefficient = int(form_data["coefficient"])
            semester = form_data["semester"]
            from datetime import date

            new_grade = {
                "subject": subject,
                "grade": grade,
                "coefficient": coefficient,
                "date": date.today().strftime("%Y-%m-%d"),
                "semester": semester,
            }
            for student in self.students_grades:
                if student["id"] == student_id:
                    student["grades"].append(new_grade)
                    break
            self.is_updating = False
            yield rx.toast("Nouvelle note ajoutée avec succès!")
        except Exception as e:
            self.is_updating = False
            logging.exception(f"Error adding grade: {e}")
            yield rx.toast(
                "Erreur lors de l'ajout de la note",
                style={"background": "#F87171", "color": "white"},
            )