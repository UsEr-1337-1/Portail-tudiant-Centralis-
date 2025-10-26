import reflex as rx
from app.components.sidebar import page_layout
from app.states.requests_state import RequestsState
from app.states.auth_state import AuthState
from app.states.admin_state import AdminState


def request_form() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Nouvelle Demande", class_name="text-xl font-bold text-gray-800 mb-6"),
        rx.el.form(
            rx.el.div(
                rx.el.label(
                    "Type de document",
                    class_name="block text-sm font-semibold text-gray-700 mb-2",
                ),
                rx.el.select(
                    rx.el.option("Sélectionnez un type", value="", disabled=True),
                    rx.el.option(
                        "Certificat de scolarité", value="certificat_scolarite"
                    ),
                    rx.el.option(
                        "Attestation de réussite", value="attestation_reussite"
                    ),
                    rx.el.option("Relevé de notes", value="releve_notes"),
                    rx.el.option("Convention de stage", value="convention_stage"),
                    name="request_type",
                    required=True,
                    class_name="w-full px-4 py-3 bg-white border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all duration-200",
                ),
                class_name="mb-6",
            ),
            rx.el.div(
                rx.el.label(
                    "Description (optionnelle)",
                    class_name="block text-sm font-semibold text-gray-700 mb-2",
                ),
                rx.el.textarea(
                    name="description",
                    placeholder="Précisez l'usage du document si nécessaire...",
                    rows=3,
                    class_name="w-full px-4 py-3 bg-white border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all duration-200 resize-none",
                ),
                class_name="mb-6",
            ),
            rx.el.button(
                rx.cond(
                    RequestsState.is_submitting,
                    rx.spinner(class_name="w-5 h-5 text-white"),
                    rx.el.span(
                        rx.icon("file-plus-2", class_name="w-5 h-5 mr-2"),
                        "Soumettre la demande",
                        class_name="flex items-center",
                    ),
                ),
                type="submit",
                is_disabled=RequestsState.is_submitting,
                class_name="w-full bg-teal-500 text-white font-semibold py-3 px-6 rounded-xl shadow-md hover:bg-teal-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500 transition-all duration-300 flex justify-center items-center",
            ),
            on_submit=RequestsState.submit_request,
            reset_on_submit=True,
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-100 shadow-sm mb-8",
    )


def status_badge(status: str) -> rx.Component:
    return rx.match(
        status,
        (
            "en_cours",
            rx.el.span(
                "En cours",
                class_name="px-3 py-1 bg-orange-100 text-orange-800 rounded-full text-sm font-medium w-fit",
            ),
        ),
        (
            "approuvee",
            rx.el.span(
                "Approuvée",
                class_name="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium w-fit",
            ),
        ),
        (
            "rejetee",
            rx.el.span(
                "Rejetée",
                class_name="px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm font-medium w-fit",
            ),
        ),
        rx.el.span(
            "Inconnu",
            class_name="px-3 py-1 bg-gray-100 text-gray-800 rounded-full text-sm font-medium w-fit",
        ),
    )


def requests_page() -> rx.Component:
    return page_layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Demandes Administratives",
                    class_name="text-3xl font-bold text-gray-800 mb-2",
                ),
                rx.el.p(
                    "Gérez vos demandes ou celles des étudiants",
                    class_name="text-gray-500 mb-8",
                ),
                class_name="mb-8",
            ),
            rx.cond(
                AuthState.current_user["role"] == "etudiant",
                request_form(),
                rx.el.div(),
            ),
            rx.el.div(
                rx.el.h3(
                    rx.cond(
                        AuthState.current_user["role"] == "etudiant",
                        "Historique de vos demandes",
                        "Toutes les demandes en attente",
                    ),
                    class_name="text-xl font-bold text-gray-800 mb-6",
                ),
                rx.cond(
                    RequestsState.all_requests.length() > 0,
                    rx.el.div(
                        rx.foreach(RequestsState.all_requests, admin_request_row),
                        class_name="flex flex-col gap-4",
                    ),
                    rx.el.div(
                        rx.icon("file-x", class_name="w-12 h-12 text-gray-300"),
                        rx.el.p(
                            "Aucune demande trouvée",
                            class_name="text-xl text-gray-500 mt-4",
                        ),
                        class_name="flex flex-col items-center justify-center h-40 border-2 border-dashed border-gray-300 rounded-2xl",
                    ),
                ),
                class_name="animate-fade-in",
            ),
        )
    )


def admin_request_row(request) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("file-text", class_name="w-5 h-5 text-teal-600"),
            rx.el.div(
                rx.el.h4(
                    request["type"], class_name="font-semibold text-gray-800 text-sm"
                ),
                rx.el.p(
                    f"Demandé le {request['date']}", class_name="text-xs text-gray-500"
                ),
                class_name="ml-3",
            ),
            class_name="flex items-center flex-1",
        ),
        rx.el.div(status_badge(request["status"]), class_name="flex items-center"),
        rx.match(
            AuthState.current_user["role"],
            (
                "administrateur",
                rx.cond(
                    request["status"] == "en_cours",
                    rx.el.div(
                        rx.el.button(
                            rx.icon("check", class_name="w-4 h-4"),
                            on_click=lambda: AdminState.process_request(
                                request["id"], True
                            ),
                            class_name="p-2 bg-green-100 text-green-600 rounded-lg hover:bg-green-200 transition-all duration-200",
                        ),
                        rx.el.button(
                            rx.icon("x", class_name="w-4 h-4"),
                            on_click=lambda: AdminState.process_request(
                                request["id"], False
                            ),
                            class_name="p-2 bg-red-100 text-red-600 rounded-lg hover:bg-red-200 transition-all duration-200 ml-2",
                        ),
                        class_name="flex items-center",
                    ),
                    rx.el.div(class_name="w-20 h-8"),
                ),
            ),
            (
                "etudiant",
                rx.el.div(
                    rx.cond(
                        request["status"] == "approuvee",
                        rx.el.button(
                            rx.icon("download", class_name="w-4 h-4"),
                            on_click=lambda: RequestsState.download_document(
                                request["id"]
                            ),
                            class_name="p-2 bg-teal-100 text-teal-600 rounded-lg hover:bg-teal-200 transition-all duration-200",
                        ),
                        rx.el.div(class_name="w-10 h-8"),
                    )
                ),
            ),
            rx.el.div(class_name="w-20 h-8"),
        ),
        class_name="flex items-center justify-between p-4 bg-white border border-gray-100 rounded-xl shadow-sm hover:shadow-md transition-all duration-300",
    )