import reflex as rx
from typing import TypedDict, Literal, Optional

Semester = Literal["Semestre 1", "Semestre 2", "Semestre 3", "Semestre 4"]
GradeStatus = Literal["excellent", "good", "needs_improvement", "failing"]


class Grade(TypedDict):
    id: int
    subject: str
    grade: float
    coefficient: int
    date: str
    semester: Semester


class NotesState(rx.State):
    selected_semester: str = ""
    all_grades: list[Grade] = [
        {
            "id": 1,
            "subject": "Mathématiques",
            "grade": 18.5,
            "coefficient": 4,
            "date": "2023-10-15",
            "semester": "Semestre 1",
        },
        {
            "id": 2,
            "subject": "Physique",
            "grade": 15.0,
            "coefficient": 3,
            "date": "2023-10-20",
            "semester": "Semestre 1",
        },
        {
            "id": 3,
            "subject": "Informatique",
            "grade": 16.0,
            "coefficient": 3,
            "date": "2023-10-22",
            "semester": "Semestre 1",
        },
        {
            "id": 4,
            "subject": "Anglais",
            "grade": 14.0,
            "coefficient": 2,
            "date": "2023-11-05",
            "semester": "Semestre 1",
        },
        {
            "id": 5,
            "subject": "Histoire",
            "grade": 12.5,
            "coefficient": 2,
            "date": "2023-11-10",
            "semester": "Semestre 1",
        },
        {
            "id": 6,
            "subject": "Mathématiques",
            "grade": 17.0,
            "coefficient": 4,
            "date": "2024-03-12",
            "semester": "Semestre 2",
        },
        {
            "id": 7,
            "subject": "Physique",
            "grade": 13.5,
            "coefficient": 3,
            "date": "2024-03-18",
            "semester": "Semestre 2",
        },
        {
            "id": 8,
            "subject": "Informatique",
            "grade": 19.0,
            "coefficient": 3,
            "date": "2024-03-20",
            "semester": "Semestre 2",
        },
    ]

    @rx.var
    def general_average(self) -> float:
        if not self.all_grades:
            return 0.0
        total_points = sum((g["grade"] * g["coefficient"] for g in self.all_grades))
        total_coeffs = sum((g["coefficient"] for g in self.all_grades))
        return total_points / total_coeffs if total_coeffs > 0 else 0.0

    @rx.var
    def recent_grades(self) -> list[Grade]:
        return sorted(self.all_grades, key=lambda g: g["date"], reverse=True)[:5]

    @rx.var
    def filtered_grades(self) -> list[Grade]:
        if not self.selected_semester:
            return self.all_grades
        return [g for g in self.all_grades if g["semester"] == self.selected_semester]

    @rx.event
    def get_grade_status(self, grade: float) -> GradeStatus:
        if grade >= 16:
            return "excellent"
        if grade >= 14:
            return "good"
        if grade >= 10:
            return "needs_improvement"
        return "failing"