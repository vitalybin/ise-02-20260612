from domain.enums import Berechtigung
from domain.user import User


class BerechtigungsService:
    def execute(self, user: User, berechtigung: Berechtigung) -> None:
        if not user or not user.active:
            raise PermissionError("Benutzer ist nicht aktiv oder nicht angemeldet")
        if not user.besitztBerechtigung(berechtigung):
            raise PermissionError(
                f"Benutzer '{user.username}' hat keine Berechtigung: {berechtigung.value}"
            )
