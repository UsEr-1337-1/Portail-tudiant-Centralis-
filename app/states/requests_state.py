import reflex as rx
from typing import TypedDict, Literal

RequestStatus = Literal["en_cours", "approuvee", "rejetee"]


class Request(TypedDict):
    id: int
    type: str
    status: RequestStatus
    date: str


import asyncio
import datetime


class RequestsState(rx.State):
    all_requests: list[Request] = [
        {
            "id": 1,
            "type": "Certificat de scolarité",
            "status": "approuvee",
            "date": "2024-05-10",
        },
        {
            "id": 2,
            "type": "Relevé de notes",
            "status": "en_cours",
            "date": "2024-05-20",
        },
        {
            "id": 3,
            "type": "Attestation de réussite",
            "status": "rejetee",
            "date": "2024-04-15",
        },
        {
            "id": 4,
            "type": "Convention de stage",
            "status": "en_cours",
            "date": "2024-05-22",
        },
    ]
    is_submitting: bool = False

    @rx.var
    def pending_requests_count(self) -> int:
        return len([r for r in self.all_requests if r["status"] == "en_cours"])

    @rx.event
    async def submit_request(self, form_data: dict):
        self.is_submitting = True
        yield
        await asyncio.sleep(1)
        new_request = {
            "id": len(self.all_requests) + 1,
            "type": form_data["request_type"].replace("_", " ").capitalize(),
            "status": "en_cours",
            "date": datetime.date.today().strftime("%Y-%m-%d"),
            "description": form_data.get("description", ""),
        }
        self.all_requests.insert(0, new_request)
        self.is_submitting = False
        yield rx.toast("Votre demande a été soumise avec succès !")

    @rx.event
    def download_document(self, request_id: int):
        request = next((r for r in self.all_requests if r["id"] == request_id), None)
        if request:
            return rx.toast(f"Téléchargement du document : {request['type']}")