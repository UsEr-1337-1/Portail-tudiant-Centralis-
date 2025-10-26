import reflex as rx
from typing import TypedDict, Literal
import datetime
from app.states.auth_state import AuthState, User


class Message(TypedDict):
    sender: str
    content: str
    timestamp: str
    is_read: bool


class Conversation(TypedDict):
    id: int
    participants: list[str]
    messages: list[Message]
    is_read: bool
    last_message_time: str


class MessagingState(rx.State):
    conversations: list[Conversation] = [
        {
            "id": 1,
            "participants": ["Jean Dupont", "Marie Curie"],
            "messages": [
                {
                    "sender": "Marie Curie",
                    "content": "Bonjour Jean, avez-vous pu avancer sur le projet ?",
                    "timestamp": "2024-05-27T10:00:00",
                    "is_read": True,
                },
                {
                    "sender": "Jean Dupont",
                    "content": "Bonjour Professeur, oui j'ai presque terminé. Je vous envoie ça demain.",
                    "timestamp": "2024-05-27T10:05:00",
                    "is_read": True,
                },
            ],
            "is_read": True,
            "last_message_time": "2024-05-27T10:05:00",
        },
        {
            "id": 2,
            "participants": ["Jean Dupont", "Louis Pasteur"],
            "messages": [
                {
                    "sender": "Louis Pasteur",
                    "content": "Votre demande de certificat a été approuvée. Vous pouvez la télécharger.",
                    "timestamp": "2024-05-26T14:30:00",
                    "is_read": False,
                }
            ],
            "is_read": False,
            "last_message_time": "2024-05-26T14:30:00",
        },
    ]
    selected_conversation_id: int = 1
    show_new_message_modal: bool = False

    @rx.var
    def unread_messages_count(self) -> int:
        return len([c for c in self.conversations if not c["is_read"]])

    @rx.var
    def current_conversation(self) -> Conversation | None:
        for conv in self.conversations:
            if conv["id"] == self.selected_conversation_id:
                return conv
        return None

    @rx.var
    def conversations_list(self) -> list[Conversation]:
        return sorted(
            self.conversations, key=lambda c: c["last_message_time"], reverse=True
        )

    @rx.event
    def select_conversation(self, conversation_id: int):
        self.selected_conversation_id = conversation_id
        self.mark_conversation_as_read(conversation_id)

    @rx.event
    def mark_conversation_as_read(self, conversation_id: int):
        for i, conv in enumerate(self.conversations):
            if conv["id"] == conversation_id:
                self.conversations[i]["is_read"] = True
                break

    @rx.event
    async def send_message(self, form_data: dict):
        message_content = form_data.get("message", "").strip()
        if not message_content or self.current_conversation is None:
            return
        auth_state = await self.get_state(AuthState)
        current_user_name = auth_state.current_user["name"]
        new_message = {
            "sender": current_user_name,
            "content": message_content,
            "timestamp": datetime.datetime.now().isoformat(),
            "is_read": True,
        }
        for i, conv in enumerate(self.conversations):
            if conv["id"] == self.selected_conversation_id:
                self.conversations[i]["messages"].append(new_message)
                self.conversations[i]["last_message_time"] = new_message["timestamp"]
                break
        yield rx.set_value("message_input", "")

    @rx.event
    def start_new_conversation(self, form_data: dict):
        self.toggle_new_message_modal()
        yield rx.toast("Nouvelle conversation démarrée (simulation).")

    @rx.event
    def toggle_new_message_modal(self):
        self.show_new_message_modal = not self.show_new_message_modal