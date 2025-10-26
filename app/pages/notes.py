import reflex as rx
from app.components.sidebar import page_layout
from app.states.notes_state import NotesState


def grade_card(grade) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    grade["subject"],
                    class_name="font-semibold text-gray-800 text-lg mb-1",
                ),
                rx.el.p(
                    f"Coefficient: {grade['coefficient']}",
                    class_name="text-sm text-gray-500",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.el.div(
                    f"{grade['grade']:.1f}",
                    class_name=rx.match(
                        NotesState.get_grade_status(grade["grade"]),
                        (
                            "excellent",
                            "bg-green-100 text-green-800 px-3 py-2 rounded-xl font-bold text-lg",
                        ),
                        (
                            "good",
                            "bg-blue-100 text-blue-800 px-3 py-2 rounded-xl font-bold text-lg",
                        ),
                        (
                            "needs_improvement",
                            "bg-orange-100 text-orange-800 px-3 py-2 rounded-xl font-bold text-lg",
                        ),
                        (
                            "failing",
                            "bg-red-100 text-red-800 px-3 py-2 rounded-xl font-bold text-lg",
                        ),
                        "bg-gray-100 text-gray-800 px-3 py-2 rounded-xl font-bold text-lg",
                    ),
                ),
                rx.el.p(grade["date"], class_name="text-xs text-gray-500 mt-2"),
                class_name="text-right",
            ),
            class_name="flex justify-between items-start",
        ),
        rx.el.div(
            rx.el.span(
                grade["semester"],
                class_name="px-2 py-1 bg-teal-100 text-teal-700 rounded-lg text-xs font-medium",
            ),
            class_name="mt-3",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-all duration-300",
    )


def statistics_card() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Statistiques", class_name="text-xl font-bold text-gray-800 mb-6"),
        rx.el.div(
            rx.el.div(
                rx.icon("trending-up", class_name="w-6 h-6 text-teal-600 mb-2"),
                rx.el.p("Moyenne Générale", class_name="text-sm text-gray-600 mb-1"),
                rx.el.p(
                    f"{NotesState.general_average:.2f} / 20",
                    class_name="text-2xl font-bold text-teal-600",
                ),
                class_name="text-center",
            ),
            rx.el.div(
                rx.icon("award", class_name="w-6 h-6 text-green-600 mb-2"),
                rx.el.p("Meilleures Notes", class_name="text-sm text-gray-600 mb-1"),
                rx.el.p(
                    "5 excellentes", class_name="text-lg font-semibold text-green-600"
                ),
                class_name="text-center",
            ),
            rx.el.div(
                rx.icon("book-open", class_name="w-6 h-6 text-blue-600 mb-2"),
                rx.el.p("Total Matières", class_name="text-sm text-gray-600 mb-1"),
                rx.el.p("5 matières", class_name="text-lg font-semibold text-blue-600"),
                class_name="text-center",
            ),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-6",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-100 shadow-sm mb-6",
    )


def semester_filter() -> rx.Component:
    return rx.el.div(
        rx.el.label(
            "Filtrer par semestre:",
            class_name="block text-sm font-semibold text-gray-700 mb-2",
        ),
        rx.el.select(
            rx.el.option("Tous les semestres", value=""),
            rx.el.option("Semestre 1", value="Semestre 1"),
            rx.el.option("Semestre 2", value="Semestre 2"),
            rx.el.option("Semestre 3", value="Semestre 3"),
            rx.el.option("Semestre 4", value="Semestre 4"),
            value=NotesState.selected_semester,
            on_change=NotesState.set_selected_semester,
            class_name="px-4 py-3 bg-white border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all duration-200 min-w-48",
        ),
        class_name="mb-6",
    )


def notes_page() -> rx.Component:
    return page_layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Mes Notes", class_name="text-3xl font-bold text-gray-800 mb-2"
                ),
                rx.el.p(
                    "Consultez toutes vos notes par semestre et matière",
                    class_name="text-gray-500 mb-8",
                ),
                class_name="mb-8",
            ),
            statistics_card(),
            semester_filter(),
            rx.el.div(
                rx.cond(
                    NotesState.filtered_grades.length() > 0,
                    rx.el.div(
                        rx.foreach(NotesState.filtered_grades, grade_card),
                        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                    ),
                    rx.el.div(
                        rx.icon("search-x", class_name="w-12 h-12 text-gray-300"),
                        rx.el.p(
                            "Aucune note trouvée pour ce semestre",
                            class_name="text-xl text-gray-500 mt-4",
                        ),
                        class_name="flex flex-col items-center justify-center h-40 border-2 border-dashed border-gray-300 rounded-2xl",
                    ),
                ),
                class_name="animate-fade-in",
            ),
        )
    )