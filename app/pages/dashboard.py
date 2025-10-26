import reflex as rx
from app.components.sidebar import page_layout
from app.states.auth_state import AuthState
from app.states.notes_state import NotesState, Grade
from app.states.schedule_state import ScheduleState
from app.states.requests_state import RequestsState


def dashboard_card(icon: str, title: str, value: str | int, color: str) -> rx.Component:
    base_class = "p-3 rounded-full"
    color_class = rx.cond(
        color == "teal",
        "bg-teal-100 text-teal-600",
        rx.cond(
            color == "blue",
            "bg-blue-100 text-blue-600",
            "bg-orange-100 text-orange-600",
        ),
    )
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="w-6 h-6"), class_name=[base_class, color_class]
        ),
        rx.el.p(title, class_name="text-md font-medium text-gray-600 mt-4"),
        rx.el.p(value, class_name="text-2xl font-bold text-gray-800"),
        class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-300",
    )


def grade_badge(grade: Grade) -> rx.Component:
    return rx.el.div(
        rx.el.p(grade["subject"], class_name="font-medium text-sm text-gray-700"),
        rx.el.div(
            rx.el.p(f"{grade['grade']:.2f}", class_name="font-bold text-sm"),
            class_name=rx.match(
                NotesState.get_grade_status(grade["grade"]),
                ("excellent", "px-2 py-1 rounded-full bg-green-100 text-green-800"),
                ("good", "px-2 py-1 rounded-full bg-blue-100 text-blue-800"),
                (
                    "needs_improvement",
                    "px-2 py-1 rounded-full bg-orange-100 text-orange-800",
                ),
                ("failing", "px-2 py-1 rounded-full bg-red-100 text-red-800"),
                "px-2 py-1 rounded-full bg-gray-100 text-gray-800",
            ),
        ),
        class_name="flex items-center justify-between p-2 border-b border-gray-100",
    )


def recent_grades_card() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Notes Récentes", class_name="font-semibold text-gray-800 mb-3"),
        rx.foreach(NotesState.recent_grades, grade_badge),
        class_name="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm col-span-1",
    )


def schedule_today_card() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Emploi du temps du jour", class_name="font-semibold text-gray-800 mb-3"
        ),
        rx.cond(
            ScheduleState.today_classes.length() == 0,
            rx.el.div(
                rx.icon("calendar-check-2", class_name="w-8 h-8 text-gray-300"),
                rx.el.p("Aucun cours aujourd'hui", class_name="text-gray-500 mt-2"),
                class_name="flex flex-col items-center justify-center h-full text-center text-sm py-4",
            ),
            rx.el.div(
                rx.foreach(
                    ScheduleState.today_classes,
                    lambda course: rx.el.div(
                        rx.el.div(
                            rx.el.p(
                                course["start_time"],
                                class_name="font-semibold text-xs text-teal-700",
                            ),
                            rx.el.p(
                                course["end_time"], class_name="text-xs text-gray-500"
                            ),
                            class_name="w-16 text-center",
                        ),
                        rx.el.div(class_name="w-1 h-full", bg=course["color"]),
                        rx.el.div(
                            rx.el.p(
                                course["subject"],
                                class_name="font-bold text-gray-800 text-sm",
                            ),
                            rx.el.p(
                                f"{course['professor']} - Salle {course['room']}",
                                class_name="text-xs text-gray-500",
                            ),
                            class_name="pl-3",
                        ),
                        class_name="flex items-center gap-3 p-2",
                    ),
                ),
                class_name="flex flex-col gap-2",
            ),
        ),
        class_name="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm col-span-1 lg:col-span-2",
    )


def dashboard_page() -> rx.Component:
    return page_layout(
        rx.el.div(
            rx.el.h1(
                f"Bienvenue, {AuthState.current_user['name']}!",
                class_name="text-3xl font-bold text-gray-800 mb-2",
            ),
            rx.el.p(
                "Voici un aperçu de votre situation académique.",
                class_name="text-gray-500 mb-8",
            ),
            rx.el.div(
                dashboard_card(
                    "award",
                    "Moyenne Générale",
                    f"{NotesState.general_average:.2f} / 20",
                    "teal",
                ),
                dashboard_card("book-check", "Crédits Validés", "120 ECTS", "blue"),
                dashboard_card(
                    "file-text",
                    "Demandes en cours",
                    RequestsState.pending_requests_count,
                    "orange",
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
            ),
            rx.el.div(
                schedule_today_card(),
                recent_grades_card(),
                class_name="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6",
            ),
            rx.match(
                AuthState.current_user["role"],
                (
                    "etudiant",
                    rx.el.div(
                        rx.el.h2(
                            "Actions rapides",
                            class_name="text-2xl font-bold text-gray-800 mt-12 mb-4",
                        ),
                        rx.el.div(
                            rx.el.a(
                                rx.el.button(
                                    rx.icon("file-plus-2", class_name="mr-2 w-5 h-5"),
                                    "Nouvelle Demande",
                                    class_name="bg-teal-500 text-white px-6 py-3 rounded-xl font-semibold shadow-md hover:bg-teal-600 transition-all flex items-center",
                                ),
                                href="/requests",
                            ),
                            rx.el.a(
                                rx.el.button(
                                    rx.icon("calendar-days", class_name="mr-2 w-5 h-5"),
                                    "Mon Emploi du Temps",
                                    class_name="bg-gray-200 text-gray-800 px-6 py-3 rounded-xl font-semibold hover:bg-gray-300 transition-all flex items-center",
                                ),
                                href="/schedule",
                            ),
                            class_name="flex gap-4",
                        ),
                        class_name="mt-8",
                    ),
                ),
                (
                    "professeur",
                    rx.el.div(
                        rx.el.h2(
                            "Gestion des notes",
                            class_name="text-2xl font-bold text-gray-800 mt-12 mb-4",
                        ),
                        rx.el.p(
                            "Interface de modification des notes à venir.",
                            class_name="text-gray-500",
                        ),
                        class_name="mt-8",
                    ),
                ),
                (
                    "administrateur",
                    rx.el.div(
                        rx.el.h2(
                            "Tâches administratives",
                            class_name="text-2xl font-bold text-gray-800 mt-12 mb-4",
                        ),
                        rx.el.p(
                            "Interface de gestion des demandes et des emplois du temps à venir.",
                            class_name="text-gray-500",
                        ),
                        class_name="mt-8",
                    ),
                ),
                rx.el.div(),
            ),
            class_name="animate-fade-in",
        )
    )