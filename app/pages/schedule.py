import reflex as rx
from app.components.sidebar import page_layout
from app.states.schedule_state import ScheduleState


def class_card(course) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h4(
                    course["subject"],
                    class_name="font-semibold text-white text-sm mb-1",
                ),
                rx.el.p(
                    course["professor"], class_name="text-white text-xs opacity-90 mb-1"
                ),
                rx.el.p(
                    f"Salle {course['room']}",
                    class_name="text-white text-xs opacity-75",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.el.p(
                    course["start_time"], class_name="text-white text-xs font-medium"
                ),
                rx.el.p(course["end_time"], class_name="text-white text-xs opacity-75"),
                class_name="text-right",
            ),
            class_name="flex justify-between items-start",
        ),
        class_name=f"p-3 rounded-xl shadow-md text-white transition-all duration-300 hover:shadow-lg hover:-translate-y-1",
        style={"background-color": course["color"]},
    )


def daily_schedule(day_name: str, day_index: int) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                day_name, class_name="font-semibold text-gray-800 text-center mb-4"
            ),
            class_name="border-b border-gray-200 pb-2 mb-4",
        ),
        rx.el.div(
            rx.cond(
                ScheduleState.classes_by_day[day_index].length() > 0,
                rx.el.div(
                    rx.foreach(ScheduleState.classes_by_day[day_index], class_card),
                    class_name="flex flex-col gap-3",
                ),
                rx.el.div(
                    rx.icon("calendar-x", class_name="w-6 h-6 text-gray-300"),
                    rx.el.p("Pas de cours", class_name="text-xs text-gray-400 mt-2"),
                    class_name="flex flex-col items-center justify-center h-20 text-center",
                ),
            ),
            class_name="min-h-32",
        ),
        class_name="bg-white p-4 rounded-xl border border-gray-100 shadow-sm",
    )


def week_navigation() -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.icon("chevron-left", class_name="w-5 h-5"),
            "Semaine précédente",
            on_click=ScheduleState.previous_week,
            class_name="flex items-center gap-2 px-4 py-2 bg-gray-100 text-gray-700 rounded-xl hover:bg-gray-200 transition-all duration-200 font-medium",
        ),
        rx.el.div(
            rx.el.p(
                f"Semaine du {ScheduleState.current_week_start}",
                class_name="font-semibold text-gray-800",
            ),
            class_name="flex items-center",
        ),
        rx.el.button(
            "Semaine suivante",
            rx.icon("chevron-right", class_name="w-5 h-5"),
            on_click=ScheduleState.next_week,
            class_name="flex items-center gap-2 px-4 py-2 bg-teal-500 text-white rounded-xl hover:bg-teal-600 transition-all duration-200 font-medium",
        ),
        class_name="flex justify-between items-center mb-8",
    )


def schedule_page() -> rx.Component:
    return page_layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Emploi du temps",
                    class_name="text-3xl font-bold text-gray-800 mb-2",
                ),
                rx.el.p(
                    "Consultez votre emploi du temps hebdomadaire",
                    class_name="text-gray-500 mb-8",
                ),
                class_name="mb-8",
            ),
            week_navigation(),
            rx.el.div(
                daily_schedule("Lundi", 0),
                daily_schedule("Mardi", 1),
                daily_schedule("Mercredi", 2),
                daily_schedule("Jeudi", 3),
                daily_schedule("Vendredi", 4),
                daily_schedule("Samedi", 5),
                daily_schedule("Dimanche", 6),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-7 gap-6",
            ),
        )
    )