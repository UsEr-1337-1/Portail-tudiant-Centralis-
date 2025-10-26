import reflex as rx
from app.states.auth_state import AuthState
from app.states.notifications_state import NotificationsState


def notification_icon(notification) -> rx.Component:
    return rx.match(
        notification["type"],
        ("new_message", rx.icon("message-square", class_name="w-5 h-5 text-blue-500")),
        ("grade_update", rx.icon("award", class_name="w-5 h-5 text-green-500")),
        ("request_status", rx.icon("file-check", class_name="w-5 h-5 text-teal-500")),
        (
            "schedule_change",
            rx.icon("calendar-days", class_name="w-5 h-5 text-orange-500"),
        ),
        rx.icon("bell", class_name="w-5 h-5 text-gray-500"),
    )


def notification_item(notification) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            notification_icon(notification),
            rx.el.div(
                rx.el.p(
                    notification["content"],
                    class_name="text-sm text-gray-800 font-medium",
                ),
                rx.el.p("il y a 5 minutes", class_name="text-xs text-gray-500"),
                class_name="ml-3 flex-1",
            ),
            rx.cond(
                ~notification["is_read"],
                rx.el.div(class_name="w-2 h-2 rounded-full bg-blue-500"),
                None,
            ),
            class_name="flex items-center w-full",
        ),
        href=notification["link"],
        on_click=lambda: NotificationsState.mark_as_read(notification["id"]),
        class_name="block p-3 hover:bg-gray-50 rounded-lg transition-colors",
    )


def notifications_popover() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3("Notifications", class_name="font-semibold text-gray-800"),
                rx.el.button(
                    "Tout marquer comme lu",
                    on_click=NotificationsState.mark_all_as_read,
                    class_name="text-sm text-teal-600 font-medium hover:underline",
                ),
                class_name="flex justify-between items-center p-4 border-b border-gray-200",
            ),
            rx.el.div(
                rx.cond(
                    NotificationsState.notifications.length() > 0,
                    rx.el.div(
                        rx.foreach(NotificationsState.notifications, notification_item),
                        class_name="flex flex-col",
                    ),
                    rx.el.div(
                        rx.icon("bell-off", class_name="w-10 h-10 text-gray-300"),
                        rx.el.p("Aucune notification", class_name="text-gray-500 mt-2"),
                        class_name="flex flex-col items-center justify-center h-48 text-center",
                    ),
                ),
                class_name="max-h-96 overflow-y-auto",
            ),
        ),
        class_name="absolute top-16 right-0 w-80 md:w-96 bg-white rounded-xl shadow-2xl border border-gray-100 z-50",
    )


def top_navbar() -> rx.Component:
    return rx.el.header(
        rx.el.div(),
        rx.el.div(
            rx.el.a(
                rx.icon("message-circle", class_name="w-6 h-6"),
                href="/messages",
                class_name="relative p-2 text-gray-500 hover:text-teal-600 hover:bg-teal-50 rounded-full transition-all",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("bell", class_name="w-6 h-6"),
                    rx.cond(
                        NotificationsState.unread_notifications_count > 0,
                        rx.el.span(
                            NotificationsState.unread_notifications_count.to_string(),
                            class_name="absolute -top-1 -right-1 flex items-center justify-center w-5 h-5 text-xs font-bold text-white bg-red-500 rounded-full",
                        ),
                        None,
                    ),
                    on_click=NotificationsState.toggle_notifications_popover,
                    class_name="relative p-2 text-gray-500 hover:text-teal-600 hover:bg-teal-50 rounded-full transition-all",
                ),
                rx.cond(
                    NotificationsState.show_notifications_popover,
                    notifications_popover(),
                ),
                class_name="relative ml-2",
            ),
            rx.el.div(
                rx.el.div(
                    rx.image(
                        src=f"https://api.dicebear.com/9.x/initials/svg?seed={AuthState.current_user['name']}",
                        class_name="w-10 h-10 rounded-full",
                    ),
                    rx.el.div(
                        rx.el.p(
                            AuthState.current_user["name"],
                            class_name="font-semibold text-sm text-gray-800",
                        ),
                        rx.el.p(
                            AuthState.current_user["email"],
                            class_name="text-xs text-gray-500",
                        ),
                        class_name="ml-3 hidden md:block",
                    ),
                    class_name="flex items-center",
                ),
                rx.el.button(
                    rx.icon("log-out", class_name="w-5 h-5"),
                    on_click=AuthState.logout,
                    class_name="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-full transition-all ml-4",
                ),
                class_name="flex items-center justify-between p-2 border-l border-gray-200 ml-4 pl-4",
            ),
            class_name="flex items-center",
        ),
        class_name="h-20 flex items-center justify-between px-8 border-b border-gray-200 bg-white sticky top-0 z-40",
    )