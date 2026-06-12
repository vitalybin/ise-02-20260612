from domain.repositories import IUserRepository
from domain.enums import Berechtigung, Rolle
from domain.user import User
from application.berechtigungs_service import BerechtigungsService
from werkzeug.security import generate_password_hash


class UserVerwaltenService:
    def __init__(self, user_repo: IUserRepository,
                 berechtigungs_service: BerechtigungsService):
        self.user_repo = user_repo
        self.berechtigungs_service = berechtigungs_service

    def execute(self, admin_user, aktion: str, **kwargs) -> None:
        self.berechtigungs_service.pruefeBerechtigung(admin_user, Berechtigung.USER_VERWALTEN)
        if aktion == "anlegen":
            user = User(
                username=kwargs["username"],
                passwordHash=generate_password_hash(kwargs["password"]),
                anzeigename=kwargs.get("anzeigename", kwargs["username"]),
                rolle=Rolle(kwargs.get("rolle", "VIEWER")),
                active=True,
            )
            self.user_repo.save(user)
        elif aktion == "rolle_aendern":
            user = self.user_repo.findById(kwargs["userId"])
            if not user:
                raise ValueError("Benutzer nicht gefunden")
            user.rolle = Rolle(kwargs["rolle"])
            self.user_repo.save(user)
        elif aktion == "deaktivieren":
            user = self.user_repo.findById(kwargs["userId"])
            if not user:
                raise ValueError("Benutzer nicht gefunden")
            user.active = False
            self.user_repo.save(user)
        elif aktion == "aktivieren":
            user = self.user_repo.findById(kwargs["userId"])
            if not user:
                raise ValueError("Benutzer nicht gefunden")
            user.active = True
            self.user_repo.save(user)
        elif aktion == "alle_anzeigen":
            return self.user_repo.findAll()
        else:
            raise ValueError(f"Unbekannte Aktion: {aktion}")
