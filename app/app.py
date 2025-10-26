import reflex as rx
from app.states.auth_state import AuthState
from app.pages.login import login_page
from app.pages.dashboard import dashboard_page
from app.pages.notes import notes_page
from app.pages.schedule import schedule_page
from app.pages.requests import requests_page
from app.pages.professor import professor_dashboard
from app.pages.admin import admin_dashboard
from app.pages.messaging import messaging_page
from app.pages.notifications import notifications_page
from app.states.admin_state import AdminState
from app.states.messaging_state import MessagingState
from app.states.notifications_state import NotificationsState


def index() -> rx.Component:
    return rx.cond(AuthState.is_authenticated, dashboard_page(), login_page())


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, on_load=AuthState.check_login)
app.add_page(login_page, route="/login", on_load=AuthState.check_login)
app.add_page(dashboard_page, route="/dashboard", on_load=AuthState.check_login)
app.add_page(notes_page, route="/notes", on_load=AuthState.check_login)
app.add_page(schedule_page, route="/schedule", on_load=AuthState.check_login)
app.add_page(requests_page, route="/requests", on_load=AuthState.check_login)
app.add_page(professor_dashboard, route="/professor", on_load=AuthState.check_login)
app.add_page(admin_dashboard, route="/admin", on_load=AuthState.check_login)
app.add_page(messaging_page, route="/messages", on_load=AuthState.check_login)
app.add_page(notifications_page, route="/notifications", on_load=AuthState.check_login)