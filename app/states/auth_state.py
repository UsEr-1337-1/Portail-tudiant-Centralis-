import reflex as rx
import asyncio
from typing import TypedDict, Literal

UserRole = Literal["etudiant", "professeur", "administrateur"]


class User(TypedDict):
    id: int
    email: str
    password: str
    name: str
    role: UserRole


class AuthState(rx.State):
    _users_db: list[User] = [
        {
            "id": 1,
            "email": "etudiant@univ.fr",
            "password": "password",
            "name": "Jean Dupont",
            "role": "etudiant",
        },
        {
            "id": 2,
            "email": "prof@univ.fr",
            "password": "password",
            "name": "Marie Curie",
            "role": "professeur",
        },
        {
            "id": 3,
            "email": "admin@univ.fr",
            "password": "password",
            "name": "Louis Pasteur",
            "role": "administrateur",
        },
    ]
    is_authenticated: bool = False
    is_loading: bool = False
    error_message: str = ""
    email: str = ""
    password: str = ""
    current_user: User = {
        "id": 0,
        "email": "",
        "password": "",
        "name": "Guest",
        "role": "etudiant",
    }

    @rx.event
    async def login(self, form_data: dict):
        self.is_loading = True
        self.error_message = ""
        yield
        await asyncio.sleep(1)
        email = form_data.get("email")
        password = form_data.get("password")
        user_found = None
        for user in self._users_db:
            if user["email"] == email and user["password"] == password:
                user_found = user
                break
        if user_found:
            self.current_user = user_found
            self.is_authenticated = True
            self.is_loading = False
            yield rx.redirect("/dashboard")
            return
        else:
            self.error_message = "Email ou mot de passe incorrect."
            self.is_loading = False
            yield

    @rx.event
    def logout(self):
        self.reset()
        return rx.redirect("/login")

    @rx.event
    def check_login(self):
        if not self.is_authenticated and self.router.page.path != "/login":
            return rx.redirect("/login")
        if self.is_authenticated and self.router.page.path == "/login":
            return rx.redirect("/dashboard")