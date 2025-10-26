import reflex as rx
from typing import TypedDict, Literal
import datetime

NotificationType = Literal[
    "new_message", "grade_update", "request_status", "schedule_change"
]


class Notification(TypedDict):
    id: int
    type: NotificationType
    content: str
    is_read: bool
    timestamp: str
    link: str


class NotificationsState(rx.State):
    notifications: list[Notification] = [
        {
            "id": 1,
            "type": "grade_update",
            "content": "Nouvelle note en Mathématiques : 18.5/20",
            "is_read": False,
            "timestamp": "2024-05-27T10:00:00",
            "link": "/notes",
        },
        {
            "id": 2,
            "type": "request_status",
            "content": "Votre demande de certificat a été approuvée.",
            "is_read": True,
            "timestamp": "2024-05-26T14:30:00",
            "link": "/requests",
        },
        {
            "id": 3,
            "type": "new_message",
            "content": "Nouveau message de Marie Curie.",
            "is_read": False,
            "timestamp": "2024-05-27T11:00:00",
            "link": "/messaging",
        },
    ]
    show_notifications_popover: bool = False
    selected_filter: str = "all"

    @rx.var
    def unread_notifications_count(self) -> int:
        return len([n for n in self.notifications if not n["is_read"]])

    @rx.var
    def filtered_notifications(self) -> list[Notification]:
        if self.selected_filter == "all":
            return self.notifications
        return [n for n in self.notifications if n["type"] == self.selected_filter]

    @rx.event
    def toggle_notifications_popover(self):
        self.show_notifications_popover = not self.show_notifications_popover

    @rx.event
    def mark_as_read(self, notification_id: int):
        for i, notification in enumerate(self.notifications):
            if notification["id"] == notification_id:
                self.notifications[i]["is_read"] = True
                break

    @rx.event
    def mark_all_as_read(self):
        for i in range(len(self.notifications)):
            self.notifications[i]["is_read"] = True

    @rx.event
    def delete_notification(self, notification_id: int):
        self.notifications = [
            n for n in self.notifications if n["id"] != notification_id
        ]

    @rx.event
    def set_selected_filter(self, filter_type: str):
        self.selected_filter = filter_type

    @rx.event
    def add_notification(self, type: NotificationType, content: str, link: str):
        new_id = len(self.notifications) + 1
        new_notification = {
            "id": new_id,
            "type": type,
            "content": content,
            "is_read": False,
            "timestamp": datetime.datetime.now().isoformat(),
            "link": link,
        }
        self.notifications.insert(0, new_notification)
        yield rx.toast(f"Nouvelle notification: {content}")