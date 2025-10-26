import reflex as rx
from app.components.sidebar import page_layout
from app.states.messaging_state import MessagingState
from app.states.auth_state import AuthState


def conversation_item(conversation: dict) -> rx.Component:
    return rx.el.div(
        rx.image(
            src=f"https://api.dicebear.com/9.x/initials/svg?seed={conversation['participants'][1]}",
            class_name="w-12 h-12 rounded-full",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    conversation["participants"][1],
                    class_name="font-semibold text-gray-800",
                ),
                rx.el.p(
                    conversation["last_message_time"],
                    class_name="text-xs text-gray-400",
                ),
                class_name="flex justify-between items-center",
            ),
            rx.el.p(
                conversation["messages"][-1]["content"],
                class_name="text-sm text-gray-500 truncate",
            ),
            class_name="flex-1 ml-3",
        ),
        rx.cond(
            ~conversation["is_read"],
            rx.el.div(class_name="w-3 h-3 bg-teal-500 rounded-full"),
            rx.el.div(class_name="w-3 h-3"),
        ),
        on_click=lambda: MessagingState.select_conversation(conversation["id"]),
        class_name=rx.cond(
            MessagingState.selected_conversation_id == conversation["id"],
            "flex items-center p-3 rounded-xl bg-teal-50 cursor-pointer",
            "flex items-center p-3 rounded-xl hover:bg-gray-100 cursor-pointer transition-colors",
        ),
    )


def message_bubble(message: dict) -> rx.Component:
    is_sender = message["sender"] == AuthState.current_user["name"]
    return rx.el.div(
        rx.el.div(
            rx.el.p(message["content"], class_name="text-sm"),
            rx.el.p(
                message["timestamp"], class_name="text-xs opacity-70 mt-1 text-right"
            ),
            class_name=rx.cond(
                is_sender,
                "bg-teal-500 text-white p-3 rounded-t-xl rounded-bl-xl max-w-md",
                "bg-gray-200 text-gray-800 p-3 rounded-t-xl rounded-br-xl max-w-md",
            ),
        ),
        class_name=rx.cond(
            is_sender, "flex justify-end w-full", "flex justify-start w-full"
        ),
    )


def messaging_page() -> rx.Component:
    return page_layout(
        rx.el.div(
            rx.el.aside(
                rx.el.div(
                    rx.el.h2(
                        "Messagerie", class_name="text-2xl font-bold text-gray-800"
                    ),
                    rx.el.button(
                        rx.icon("copy", class_name="w-5 h-5"),
                        on_click=MessagingState.toggle_new_message_modal,
                        class_name="p-2 text-gray-500 hover:text-teal-600 hover:bg-teal-50 rounded-full transition-all",
                    ),
                    class_name="flex justify-between items-center p-4 border-b border-gray-200 h-20",
                ),
                rx.el.div(
                    rx.el.input(
                        placeholder="Rechercher...",
                        class_name="w-full px-4 py-2 bg-gray-100 border-transparent rounded-xl focus:ring-2 focus:ring-teal-500",
                    ),
                    class_name="p-4",
                ),
                rx.el.div(
                    rx.foreach(MessagingState.conversations_list, conversation_item),
                    class_name="flex flex-col gap-2 p-2 overflow-y-auto flex-1",
                ),
                class_name="w-96 bg-white border-r border-gray-200 flex flex-col h-full",
            ),
            rx.el.section(
                rx.cond(
                    MessagingState.current_conversation,
                    rx.el.div(
                        rx.el.div(
                            rx.el.h3(
                                MessagingState.current_conversation["participants"][1],
                                class_name="font-bold text-lg text-gray-800",
                            ),
                            class_name="p-4 border-b border-gray-200 h-20 flex items-center",
                        ),
                        rx.el.div(
                            rx.foreach(
                                MessagingState.current_conversation["messages"],
                                message_bubble,
                            ),
                            class_name="flex-1 p-6 space-y-4 overflow-y-auto",
                        ),
                        rx.el.form(
                            rx.el.input(
                                id="message_input",
                                name="message",
                                placeholder="Écrivez votre message...",
                                class_name="flex-1 px-4 py-3 bg-gray-100 border-transparent rounded-full focus:ring-2 focus:ring-teal-500",
                            ),
                            rx.el.button(
                                rx.icon("send", class_name="w-6 h-6"),
                                type="submit",
                                class_name="ml-3 p-3 bg-teal-500 text-white rounded-full hover:bg-teal-600 transition-all",
                            ),
                            on_submit=MessagingState.send_message,
                            class_name="p-4 border-t border-gray-200 flex items-center",
                        ),
                        class_name="flex flex-col h-full",
                    ),
                    rx.el.div(
                        rx.icon("message-circle", class_name="w-24 h-24 text-gray-200"),
                        rx.el.p(
                            "Sélectionnez une conversation pour commencer à discuter",
                            class_name="text-gray-500 mt-4",
                        ),
                        class_name="flex flex-col items-center justify-center h-full text-center",
                    ),
                ),
                class_name="flex-1 bg-white h-full",
            ),
            class_name="flex h-full w-full bg-gray-50",
        )
    )