from domain.repositories import IGeraetRepository
from domain.enums import Berechtigung
from domain.geraete_regel_service import GeraeteRegelService
from application.berechtigungs_service import BerechtigungsService


class GeraetKonfigurierenService:
    def __init__(self, geraet_repo: IGeraetRepository,
                 regel_service: GeraeteRegelService,
                 berechtigungs_service: BerechtigungsService):
        self.geraet_repo = geraet_repo
        self.regel_service = regel_service
        self.berechtigungs_service = berechtigungs_service

    def execute(self, user, geraetId: int, **config) -> None:
        self.berechtigungs_service.pruefeBerechtigung(user, Berechtigung.GERAET_STEUERN)
        geraet = self.geraet_repo.findById(geraetId)
        if not geraet:
            raise ValueError("Geraet nicht gefunden")
        if not self.regel_service.darfGesteuertWerden(geraet):
            raise ValueError(
                f"Geraet '{geraet.name}' darf nicht konfiguriert werden"
            )
        geraet.konfigurieren(**config)
        self.geraet_repo.save(geraet)
