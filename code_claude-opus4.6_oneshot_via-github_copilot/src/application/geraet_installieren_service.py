from domain.repositories import IGeraetRepository, IRaumRepository
from domain.enums import Berechtigung
from domain.geraete_regel_service import GeraeteRegelService
from application.berechtigungs_service import BerechtigungsService


class GeraetInstallierenService:
    def __init__(self, geraet_repo: IGeraetRepository, raum_repo: IRaumRepository,
                 regel_service: GeraeteRegelService,
                 berechtigungs_service: BerechtigungsService):
        self.geraet_repo = geraet_repo
        self.raum_repo = raum_repo
        self.regel_service = regel_service
        self.berechtigungs_service = berechtigungs_service

    def execute(self, user, geraetId: int, raumId: int) -> None:
        self.berechtigungs_service.execute(user, Berechtigung.GERAET_INSTALLIEREN)
        geraet = self.geraet_repo.findById(geraetId)
        raum = self.raum_repo.findById(raumId)
        if not geraet:
            raise ValueError("Geraet nicht gefunden")
        if not raum:
            raise ValueError("Raum nicht gefunden")
        if not self.regel_service.darfInstalliertWerden(geraet):
            raise ValueError(
                f"Geraet '{geraet.name}' darf nicht installiert werden (Status: {geraet.status.value})"
            )
        self.regel_service.pruefeRaumZuordnung(geraet, raum)
        geraet.installieren(raum)
        self.geraet_repo.save(geraet)
