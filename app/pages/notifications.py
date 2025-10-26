import reflex as rx
from app.components.sidebar import page_layout
from app.states.notifications_state import NotificationsState


def filter_button(text: str, filter_type: str) -> rx.Component:
    is_active = NotificationsState.selected_filter == filter_type
    return rx.el.button(
        text,
        on_click=lambda: NotificationsState.set_selected_filter(filter_type),
        class_name=rx.cond(
            is_active,
            "px-4 py-2 text-sm font-semibold text-white bg-teal-600 rounded-full shadow-md",
            "px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-full transition-colors",
        ),
    )


def notification_icon(notification) -> rx.Component:
    return rx.el.div(
        rx.match(
            notification["type"],
            (
                "new_message",
                rx.icon("message-square", class_name="w-5 h-5 text-blue-500"),
            ),
            ("grade_update", rx.icon("award", class_name="w-5 h-5 text-green-500")),
            (
                "request_status",
                rx.icon("file-check", class_name="w-5 h-5 text-teal-500"),
            ),
            (
                "schedule_change",
                rx.icon("calendar-days", class_name="w-5 h-5 text-orange-500"),
            ),
            rx.icon("bell", class_name="w-5 h-5 text-gray-500"),
        ),
        class_name="p-3 bg-gray-100 rounded-full",
    )


def notification_list_item(notification) -> rx.Component:
    return rx.el.div(
        notification_icon(notification),
        rx.el.div(
            rx.el.p(
                notification["content"], class_name="text-sm text-gray-800 font-medium"
            ),
            rx.el.p(notification["timestamp"], class_name="text-xs text-gray-500 mt-1"),
            class_name="ml-4 flex-1",
        ),
        rx.cond(
            ~notification["is_read"],
            rx.el.div(class_name="w-2.5 h-2.5 bg-blue-500 rounded-full mr-4"),
            rx.el.div(class_name="w-2.5 h-2.5 mr-4"),
        ),
        rx.el.button(
            rx.icon("x", class_name="w-4 h-4"),
            on_click=lambda: NotificationsState.delete_notification(notification["id"]),
            class_name="p-2 text-gray-400 hover:text-red-600 hover:bg-red-100 rounded-full transition-colors",
        ),
        class_name="flex items-center p-4 bg-white border border-gray-100 rounded-xl shadow-sm hover:shadow-md transition-all",
    )


def notifications_page() -> rx.Component:
    return page_layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Notifications", class_name="text-3xl font-bold text-gray-800"
                ),
                rx.el.button(
                    "Tout marquer comme lu",
                    on_click=NotificationsState.mark_all_as_read,
                    class_name="text-sm font-semibold text-teal-600 hover:underline",
                ),
            ),
            rx.el.p(
                "Gérez vos alertes et communications récentes.",
                class_name="text-gray-500 mb-8",
            ),
            rx.el.div(
                filter_button("Toutes", "all"),
                filter_button("Messages", "new_message"),
                filter_button("Notes", "grade_update"),
                filter_button("Demandes", "request_status"),
                filter_button("Emploi du temps", "schedule_change"),
                class_name="flex gap-3 mb-8",
            ),
            rx.cond(
                NotificationsState.filtered_notifications.length() > 0,
                rx.el.div(
                    rx.foreach(
                        NotificationsState.filtered_notifications,
                        notification_list_item,
                        key="id",
                    ),
                    class_name="flex flex-col gap-4",
                ),
                rx.el.div(
                    rx.icon("bell-off", class_name="w-16 h-16 text-gray-300"),
                    rx.el.p(
                        "Aucune notification pour le moment.",
                        class_name="text-gray-500 mt-4",
                    ),
                    class_name="flex flex-col items-center justify-center h-64 text-center border-2 border-dashed border-gray-200 rounded-2xl",
                ),
            ),
            class_name="max-w-4xl mx-auto",
        )
    )