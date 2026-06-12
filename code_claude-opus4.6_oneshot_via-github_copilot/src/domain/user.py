from domain.enums import Rolle, Berechtigung, ROLLEN_BERECHTIGUNGEN


class User:
    def __init__(self, userId: int = None, username: str = "",
                 passwordHash: str = "", anzeigename: str = "",
                 rolle: Rolle = Rolle.VIEWER, active: bool = True):
        self.userId: int = userId
        self.username: str = username
        self.passwordHash: str = passwordHash
        self.anzeigename: str = anzeigename
        self.rolle: Rolle = rolle
        self.active: bool = active

    def besitztBerechtigung(self, berechtigung: Berechtigung) -> bool:
        return berechtigung in ROLLEN_BERECHTIGUNGEN.get(self.rolle, set())
