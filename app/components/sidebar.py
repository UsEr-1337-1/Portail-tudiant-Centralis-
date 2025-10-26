import reflex as rx
from app.states.auth_state import AuthState
from app.states.messaging_state import MessagingState
from app.states.notifications_state import (
    NotificationsState,
)


def nav_item(
    icon: str,
    text: str,
    href: str,
    is_active: bool,
    badge_count: rx.Var[int] | None = None,
) -> rx.Component:
    return rx.el.a(
        rx.icon(icon, class_name="w-5 h-5 mr-3"),
        rx.el.span(text, class_name="font-medium flex-1"),
        rx.cond(
            badge_count != None,
            rx.cond(
                badge_count > 0,
                rx.el.span(
                    badge_count.to_string(),
                    class_name="px-2 py-0.5 text-xs font-bold text-white bg-red-500 rounded-full",
                ),
                None,
            ),
            None,
        ),
        href=href,
        href=href,
        class_name=rx.cond(
            is_active,
            "flex items-center p-3 rounded-lg text-white bg-teal-600 shadow-md",
            "flex items-center p-3 rounded-lg text-gray-700 hover:bg-teal-50 hover:text-teal-700 transition-colors duration-200",
        ),
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "school",
                    class_name="w-8 h-8 text-teal-500",
                ),
                rx.el.span(
                    "Portail Unifié",
                    class_name="text-xl font-bold text-gray-800 tracking-tight",
                ),
                class_name="flex items-center gap-3 h-20 px-6 border-b border-gray-200",
            ),
            rx.el.nav(
                rx.el.div(
                    rx.match(
                        AuthState.current_user["role"],
                        (
                            "etudiant",
                            rx.el.div(
                                nav_item(
                                    "layout-dashboard",
                                    "Dashboard",
                                    "/dashboard",
                                    AuthState.router.page.path
                                    == "/dashboard",
                                ),
                                nav_item(
                                    "book-marked",
                                    "Mes Notes",
                                    "/notes",
                                    AuthState.router.page.path
                                    == "/notes",
                                ),
                                nav_item(
                                    "calendar-days",
                                    "Emploi du temps",
                                    "/schedule",
                                    AuthState.router.page.path
                                    == "/schedule",
                                ),
                                nav_item(
                                    "file-text",
                                    "Mes Demandes",
                                    "/requests",
                                    AuthState.router.page.path
                                    == "/requests",
                                ),
                                nav_item(
                                    "message-circle",
                                    "Messages",
                                    "/messages",
                                    AuthState.router.page.path
                                    == "/messages",
                                    badge_count=MessagingState.unread_messages_count,
                                ),
                                nav_item(
                                    "bell",
                                    "Notifications",
                                    "/notifications",
                                    AuthState.router.page.path
                                    == "/notifications",
                                    badge_count=NotificationsState.unread_notifications_count,
                                ),
                                class_name="flex flex-col gap-2",
                            ),
                        ),
                        (
                            "professeur",
                            rx.el.div(
                                nav_item(
                                    "layout-dashboard",
                                    "Dashboard",
                                    "/professor",
                                    AuthState.router.page.path
                                    == "/professor",
                                ),
                                nav_item(
                                    "message-circle",
                                    "Messages",
                                    "/messages",
                                    AuthState.router.page.path
                                    == "/messages",
                                    badge_count=MessagingState.unread_messages_count,
                                ),
                                nav_item(
                                    "bell",
                                    "Notifications",
                                    "/notifications",
                                    AuthState.router.page.path
                                    == "/notifications",
                                    badge_count=NotificationsState.unread_notifications_count,
                                ),
                                class_name="flex flex-col gap-2",
                            ),
                        ),
                        (
                            "administrateur",
                            rx.el.div(
                                nav_item(
                                    "layout-dashboard",
                                    "Dashboard Admin",
                                    "/admin",
                                    AuthState.router.page.path
                                    == "/admin",
                                ),
                                nav_item(
                                    "message-circle",
                                    "Messages",
                                    "/messages",
                                    AuthState.router.page.path
                                    == "/messages",
                                    badge_count=MessagingState.unread_messages_count,
                                ),
                                nav_item(
                                    "bell",
                                    "Notifications",
                                    "/notifications",
                                    AuthState.router.page.path
                                    == "/notifications",
                                    badge_count=NotificationsState.unread_notifications_count,
                                ),
                                class_name="flex flex-col gap-2",
                            ),
                        ),
                        rx.el.div(),
                    ),
                    class_name="p-4",
                ),
                class_name="flex-1 overflow-y-auto",
            ),
            class_name="w-72 border-r border-gray-200 bg-white flex-shrink-0 flex flex-col",
        )
    )


from app.components.navbar import top_navbar


def page_layout(content: rx.Component) -> rx.Component:
    return rx.el.div(
        rx.cond(
            AuthState.is_authenticated,
            rx.el.div(
                sidebar(),
                rx.el.div(
                    top_navbar(),
                    rx.el.main(
                        content,
                        class_name="p-8 overflow-y-auto bg-gray-50",
                    ),
                    class_name="flex-1 flex flex-col h-screen",
                ),
                class_name="flex h-screen w-screen",
            ),
            content,
        ),
        class_name="font-['Montserrat']",
    )