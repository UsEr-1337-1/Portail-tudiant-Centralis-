import reflex as rx
from app.components.sidebar import page_layout
from app.states.admin_state import AdminState
from app.states.requests_state import RequestsState
from app.states.schedule_state import ScheduleState
from app.states.auth_state import AuthState


def admin_request_card(request) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("file-text", class_name="w-6 h-6 text-teal-600 mb-4"),
            rx.el.div(
                rx.el.h4(
                    request["type"],
                    class_name="font-semibold text-gray-800 text-lg mb-2",
                ),
                rx.el.div(
                    rx.el.span(
                        f"Demandé le {request['date']}",
                        class_name="text-sm text-gray-500",
                    ),
                    rx.el.span(
                        f"ID: #{request['id']}", class_name="text-sm text-gray-400 ml-4"
                    ),
                    class_name="flex items-center",
                ),
            ),
        ),
        rx.cond(
            request["status"] == "en_cours",
            rx.el.div(
                rx.el.button(
                    rx.icon("check", class_name="w-5 h-5 mr-2"),
                    "Approuver",
                    on_click=lambda: AdminState.process_request(request["id"], True),
                    class_name="flex items-center px-4 py-2 bg-green-500 text-white rounded-xl hover:bg-green-600 transition-all duration-200 mr-3",
                ),
                rx.el.button(
                    rx.icon("x", class_name="w-5 h-5 mr-2"),
                    "Rejeter",
                    on_click=lambda: AdminState.process_request(request["id"], False),
                    class_name="flex items-center px-4 py-2 bg-red-500 text-white rounded-xl hover:bg-red-600 transition-all duration-200",
                ),
                class_name="flex items-center",
            ),
            rx.el.div(
                rx.match(
                    request["status"],
                    (
                        "approuvee",
                        rx.el.span(
                            "Approuvée",
                            class_name="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium",
                        ),
                    ),
                    (
                        "rejetee",
                        rx.el.span(
                            "Rejetée",
                            class_name="px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm font-medium",
                        ),
                    ),
                    rx.el.span(
                        request["status"],
                        class_name="px-3 py-1 bg-gray-100 text-gray-800 rounded-full text-sm font-medium",
                    ),
                )
            ),
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-all duration-300 flex items-center justify-between",
    )


def schedule_management_card() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Gestion des Emplois du Temps",
            class_name="text-xl font-bold text-gray-800 mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("calendar-plus", class_name="w-8 h-8 text-teal-600 mb-3"),
                rx.el.h4(
                    "Ajouter un cours", class_name="font-semibold text-gray-800 mb-2"
                ),
                rx.el.p(
                    "Planifier de nouveaux créneaux", class_name="text-sm text-gray-500"
                ),
                class_name="text-center p-6 border-2 border-dashed border-gray-200 rounded-xl hover:border-teal-300 hover:bg-teal-50 transition-all duration-200 cursor-pointer",
            ),
            rx.el.div(
                rx.icon("disc_3", class_name="w-8 h-8 text-blue-600 mb-3"),
                rx.el.h4(
                    "Modifier les cours", class_name="font-semibold text-gray-800 mb-2"
                ),
                rx.el.p(
                    "Ajuster les horaires existants", class_name="text-sm text-gray-500"
                ),
                class_name="text-center p-6 border-2 border-dashed border-gray-200 rounded-xl hover:border-blue-300 hover:bg-blue-50 transition-all duration-200 cursor-pointer",
            ),
            rx.el.div(
                rx.icon("trash-2", class_name="w-8 h-8 text-red-600 mb-3"),
                rx.el.h4(
                    "Supprimer des cours", class_name="font-semibold text-gray-800 mb-2"
                ),
                rx.el.p("Annuler des créneaux", class_name="text-sm text-gray-500"),
                class_name="text-center p-6 border-2 border-dashed border-gray-200 rounded-xl hover:border-red-300 hover:bg-red-50 transition-all duration-200 cursor-pointer",
            ),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-6",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-100 shadow-sm mb-8",
    )


def stats_dashboard() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("file-clock", class_name="w-6 h-6 text-orange-600"),
                rx.el.p("Demandes en attente", class_name="text-sm text-gray-600 mt-2"),
                rx.el.p(
                    RequestsState.pending_requests_count,
                    class_name="text-2xl font-bold text-orange-600 mt-1",
                ),
                class_name="bg-white p-6 rounded-xl border border-gray-100 shadow-sm text-center",
            ),
            rx.el.div(
                rx.icon("calendar", class_name="w-6 h-6 text-teal-600"),
                rx.el.p("Cours programmés", class_name="text-sm text-gray-600 mt-2"),
                rx.el.p(
                    ScheduleState.full_schedule.length(),
                    class_name="text-2xl font-bold text-teal-600 mt-1",
                ),
                class_name="bg-white p-6 rounded-xl border border-gray-100 shadow-sm text-center",
            ),
            rx.el.div(
                rx.icon("users", class_name="w-6 h-6 text-blue-600"),
                rx.el.p("Étudiants actifs", class_name="text-sm text-gray-600 mt-2"),
                rx.el.p("125", class_name="text-2xl font-bold text-blue-600 mt-1"),
                class_name="bg-white p-6 rounded-xl border border-gray-100 shadow-sm text-center",
            ),
            rx.el.div(
                rx.icon("book-open", class_name="w-6 h-6 text-purple-600"),
                rx.el.p("Professeurs", class_name="text-sm text-gray-600 mt-2"),
                rx.el.p("15", class_name="text-2xl font-bold text-purple-600 mt-1"),
                class_name="bg-white p-6 rounded-xl border border-gray-100 shadow-sm text-center",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8",
        )
    )


def admin_dashboard() -> rx.Component:
    return page_layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    f"Administration - {AuthState.current_user['name']}",
                    class_name="text-3xl font-bold text-gray-800 mb-2",
                ),
                rx.el.p(
                    "Tableau de bord administratif", class_name="text-gray-500 mb-8"
                ),
                class_name="mb-8",
            ),
            stats_dashboard(),
            schedule_management_card(),
            rx.el.div(
                rx.el.h2(
                    "Demandes Administratives",
                    class_name="text-2xl font-bold text-gray-800 mb-6",
                ),
                rx.cond(
                    RequestsState.all_requests.length() > 0,
                    rx.el.div(
                        rx.foreach(RequestsState.all_requests, admin_request_card),
                        class_name="grid grid-cols-1 lg:grid-cols-2 gap-6",
                    ),
                    rx.el.div(
                        rx.icon("inbox", class_name="w-12 h-12 text-gray-300"),
                        rx.el.p(
                            "Aucune demande en cours",
                            class_name="text-xl text-gray-500 mt-4",
                        ),
                        class_name="flex flex-col items-center justify-center h-40 border-2 border-dashed border-gray-300 rounded-2xl",
                    ),
                ),
            ),
        )
    )