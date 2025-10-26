import reflex as rx
from app.states.auth_state import AuthState


def login_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("school", class_name="w-10 h-10 text-teal-500"),
                    rx.el.h1(
                        "Portail Étudiant",
                        class_name="text-3xl font-bold text-gray-800 tracking-tight",
                    ),
                    class_name="flex items-center gap-4 mb-8 justify-center",
                ),
                rx.el.h2(
                    "Connexion", class_name="text-2xl font-semibold text-gray-700 mb-2"
                ),
                rx.el.p(
                    "Veuillez entrer vos identifiants pour accéder à votre espace.",
                    class_name="text-gray-500 mb-8",
                ),
                rx.cond(
                    AuthState.error_message != "",
                    rx.el.div(
                        rx.icon("badge_alert", class_name="w-5 h-5 mr-3"),
                        rx.el.span(AuthState.error_message),
                        class_name="bg-red-100 border border-red-200 text-red-700 px-4 py-3 rounded-lg relative mb-6 flex items-center",
                    ),
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.label(
                            "Adresse e-mail",
                            class_name="block text-sm font-medium text-gray-700 mb-2",
                        ),
                        rx.el.input(
                            name="email",
                            type="email",
                            placeholder="nom.prenom@univ.fr",
                            class_name="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all",
                        ),
                        class_name="mb-5",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Mot de passe",
                            class_name="block text-sm font-medium text-gray-700 mb-2",
                        ),
                        rx.el.input(
                            name="password",
                            type="password",
                            placeholder="••••••••",
                            class_name="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all",
                        ),
                        class_name="mb-8",
                    ),
                    rx.el.button(
                        rx.cond(
                            AuthState.is_loading,
                            rx.spinner(class_name="text-white"),
                            rx.el.span("Se connecter"),
                        ),
                        type="submit",
                        is_disabled=AuthState.is_loading,
                        class_name="w-full bg-teal-500 text-white font-semibold py-3 rounded-lg shadow-md hover:bg-teal-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500 transition-all duration-300 flex justify-center items-center",
                    ),
                    on_submit=AuthState.login,
                ),
            ),
            class_name="w-full max-w-md p-10 bg-white rounded-2xl shadow-xl border border-gray-100",
        ),
        class_name="flex items-center justify-center min-h-screen bg-gray-50 font-['Montserrat']",
    )