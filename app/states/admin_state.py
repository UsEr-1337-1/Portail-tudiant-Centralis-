import reflex as rx
from app.states.requests_state import RequestsState, Request
from app.states.auth_state import AuthState
import logging
from app.states.notifications_state import NotificationsState


class AdminState(rx.State):
    @rx.event
    async def process_request(self, request_id: int, approved: bool):
        requests_state = await self.get_state(RequestsState)
        notifications_state = await self.get_state(NotificationsState)
        request_found = None
        for r in requests_state.all_requests:
            if r["id"] == request_id:
                request_found = r
                break
        if request_found:
            status = "approuvee" if approved else "rejetee"
            request_found["status"] = status
            if approved:
                logging.info(f"Request {request_id} approved. PDF should be generated.")
                yield rx.toast(f"Demande #{request_id} approuvée.")
            else:
                logging.info(f"Request {request_id} rejected.")
                yield rx.toast(
                    f"Demande #{request_id} rejetée.",
                    style={"background": "#F87171", "color": "white"},
                )
            yield NotificationsState.add_notification(
                type="request_status",
                content=f"Votre demande de {request_found['type']} a été {status}.",
                link="/requests",
            )
        else:
            yield rx.toast(
                f"Erreur: Demande #{request_id} non trouvée.",
                style={"background": "#F87171", "color": "white"},
            )